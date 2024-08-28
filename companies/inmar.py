import json
import requests

from . import base


class Inmar(base.Company):

    NAME = "Inmar"
    LIST_URL = "https://inmar.wd1.myworkdayjobs.com/wday/cxs/inmar/inmarcareers/jobs"
    JOB_DESC_URL = "https://inmar.wd1.myworkdayjobs.com/en-US/inmarcareers/%s"
    CATEGORY = "Engineering"
    PAGE_SIZE = 20

    def get_headers(self):
        return {
            "accept": "application/json",
            "content-type": "application/json",
        }

    def get_data(self, offset=None):
        return {
            "appliedFacets": {
                "jobFamilyGroup": ["f4d09ae81507102da2509648ba482a8e"],
                "locations": [
                    "c9856d3fa53601f8de3201b8a0010cb4",
                    "f9d9c61ccfac105075aae3e09e9a7ea2",
                ],
            },
            "limit": self.PAGE_SIZE,
            "offset": offset or 0,
            "searchText": "",
        }

    def pull(self, include_all=False):
        if include_all:
            seen = set()
        else:
            seen = self.load_seen()

        self.logger.log(f"Starting {self.NAME}. (include_all={include_all})\n")
        self.logger.log(f"Seen: {seen}\n")

        new_jobs = []

        offset = 0
        total = None
        count = 0
        while total is None or (count is not None and count < total):
            response = requests.post(
                self.LIST_URL, json=self.get_data(offset), headers=self.get_headers()
            )
            response_json = response.json()
            total = response_json.get("total")
            for item in response_json.get("jobPostings"):
                job_id = item.get("bulletFields")[0]
                if str(job_id) not in seen:
                    new_jobs.append(
                        {
                            "id": job_id,
                            "title": item.get("title"),
                            "href": item.get("externalPath"),
                            "location": item.get("locationsText"),
                            "posted": item.get("postedOn"),
                        }
                    )
                    self.mark_seen(str(job_id))
                count += 1
            offset += self.PAGE_SIZE

        return new_jobs

    def summarize(self, job):
        return """<ul>
    <li>Id: {id}</li>
    <li>Title: {title}</li>
    <li>Location: {location}</li>
    <li>Posted: {posted}</li>
    <li>URL: <a clicktracking="off" href="{url}">{title}</a></li>
    </ul>""".format(
            id=job.get("id"),
            title=job.get("title").strip(),
            location=job.get("location"),
            posted=job.get("posted"),
            url=self.JOB_DESC_URL % job.get("href"),
        )
