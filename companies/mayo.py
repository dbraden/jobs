from bs4 import BeautifulSoup
import collections
import json
import re
from selenium import webdriver

from . import base

DRIVER_WAIT = 6


class Mayo(base.Company):

    NAME = "Mayo"
    LIST_URL = "https://jobs.mayoclinic.org/search-jobs?acm=ALL&alrpm=ALL&ascf=[%7B%22key%22:%22custom_fields.RemoteField%22,%22value%22:%22Yes%22%7D]"
    JOB_DESC_URL = "https://jobs.mayoclinic.org/%s"
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

        anchor_list = soup.find(id="search-results-list")
        new_jobs = []
        for li in anchor_list.find_all("li"):
            anchor = li.find("a")
            if anchor and anchor.has_attr("data-job-id"):
                job = {
                    "id": anchor.get("data-job-id"),
                    "href": anchor.get("href"),
                    "job_title": li.find("h2").getText(),
                }
                if str(job.get("id")) in seen:
                    continue

                new_jobs.append(job)
                self.mark_seen(str(job.get("id")))

        return new_jobs

    def summarize(self, job):
        return """<ul>
    <li>Id: {id}</li>
    <li>Title: {title}</li>
    <li>URL: <a clicktracking="off" href="{url}">{title}</a></li>
    </ul>""".format(
            id=job.get("id"),
            title=job.get("job_title").strip(),
            url=self.JOB_DESC_URL % job.get("href"),
        )
