import requests

from . import base


class Honor(base.Company):

    NAME = "Honor"
    LIST_URL = "https://webmarketingapi-careers.azurewebsites.net/api/v1/honor-careers/departments?board=honor"
    JOB_DESC_URL = "https://www.honorcare.com/honor-careers/career/?jobID=%s"
    CATEGORY = "Engineering"

    def pull(self, include_all=False):
        if include_all:
            seen = set()
        else:
            seen = self.load_seen()

        self.logger.log(f"Starting {self.NAME}. (include_all={include_all})\n")
        self.logger.log(f"Seen: {seen}\n")

        response = requests.get(self.LIST_URL)
        for key, item in response.json().items():
            if item.get("name") == self.CATEGORY:
                jobs = item.get("jobs").values()
                break

        jobs = sorted(jobs, key=lambda x: x.get("posted"), reverse=True)
        new_jobs = []
        for job in jobs:
            if str(job.get("id")) not in seen:
                new_jobs.append(job)
                self.mark_seen(str(job.get("id")))

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
            location=job.get("locationName"),
            posted=job.get("posted"),
            url=self.JOB_DESC_URL % str(job.get("id")),
        )
