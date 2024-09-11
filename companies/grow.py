import requests

from . import base


class Grow(base.Company):

    NAME = "Grow"
    LIST_URL = "https://job-boards.greenhouse.io/growtherapy?departments%5B%5D=4029487005&offices%5B%5D=4011317005&_data=routes%2F%24url_token"
    JOB_DESC_URL = "https://job-boards.greenhouse.io/growtherapy/jobs/%s"
    CATEGORY = "Engineering"

    def pull(self, include_all=False):
        if include_all:
            seen = set()
        else:
            seen = self.load_seen()

        self.logger.log(f"Starting {self.NAME}. (include_all={include_all})\n")
        self.logger.log(f"Seen: {seen}\n")

        response = requests.get(self.LIST_URL)
        jobs = response.json().get('jobPosts', {}).get('data', [])
        jobs = sorted(jobs, key=lambda x: x.get("published_at"), reverse=True)
        new_jobs = []
        for job in jobs:
            if str(job.get("internal_job_id")) not in seen:
                new_jobs.append(job)
                self.mark_seen(str(job.get("internal_job_id")))

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
            posted=job.get("published_at"),
            url=self.JOB_DESC_URL % str(job.get("id")),
        )
