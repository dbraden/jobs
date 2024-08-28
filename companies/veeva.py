from bs4 import BeautifulSoup
import collections
import json
import re
from selenium import webdriver

from . import base

DRIVER_WAIT = 6


class Veeva(base.Company):

    NAME = "Veeva"
    LIST_URL = "https://careers.veeva.com/job-search-results/?search=&remote=true&ts=Engineering&regions=United+States&office_locations="
    JOB_DESC_URL = "https://careers.veeva.com/job/%s/%s"
    TEAM = "Engineering"
    REGION = "United States"

    def pull(self, include_all=False):
        if include_all:
            seen = set()
        else:
            seen = self.load_seen()

        self.logger.log(f"Starting {self.NAME}. (include_all={include_all})\n")
        self.logger.log(f"Seen: {seen}\n")

        driver = webdriver.Chrome()
        driver.implicitly_wait(DRIVER_WAIT)
        driver.get(self.LIST_URL)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        for s in soup.find_all("script"):
            rendered = s.getText()
            if "let allJobs =" in rendered:
                break

        text = rendered.replace('<script type="text/javascript">', "")
        text = re.sub("[\s]+let allJobs = ", "", text)
        text = text.replace(";", "")
        text = text.replace("</script>", "")
        data = json.loads(text)

        filtered = []
        for item in data:
            if all(
                [
                    item.get("team") == self.TEAM,
                    item.get("region") == self.REGION,
                    bool(int(item.get("remote", "0"))),
                ]
            ):
                filtered.append(item)

        new_jobs = []
        for job in filtered:
            if job.get("lever_id") in seen:
                continue

            new_jobs.append(job)
            self.mark_seen(job.get("lever_id"))

        return new_jobs

    def summarize(self, job):
        return """<ul>
    <li>Id: {id}</li>
    <li>Title: {title}</li>
    <li>Location: {location}</li>
    <li>URL: <a clicktracking="off" href="{url}">{title}</a></li>
    </ul>""".format(
            id=job.get("id"),
            title=job.get("job_title").strip(),
            location=job.get("city"),
            url=self.JOB_DESC_URL % (job.get("lever_id"), job.get("slug")),
        )
