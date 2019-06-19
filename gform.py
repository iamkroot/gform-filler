import argparse
import random
from math import ceil
from selenium import webdriver

driver = webdriver.Firefox()


def get_els(parent, role):
    return parent.find_elements_by_css_selector(f"[role='{role}']")


def fill_radios(radios):
    radio = random.choice(radios)
    if radio.find_element_by_xpath('..').text == 'Other:':
        radio = random.choice(radios[:-1])
    radio.click()


def fill_checkboxes(checks):
    n = len(checks) - 'Other' in checks[-1].get_attribute('aria-label')
    checked = random.sample(checks, k=min(ceil(random.expovariate(2 / n)), n))
    for check in checked:
        print(check.get_attribute('aria-label'))
        check.click()
    return checked


def fill_form(driver: webdriver.Firefox):
    for question in get_els(driver, 'listitem'):
        # txt = get_els(question, 'heading')[0].text
        radios = get_els(question, 'radio')
        radios and fill_radios(radios)

        checks = get_els(question, 'checkbox')
        checks and fill_checkboxes(checks)

    submit = driver.find_element_by_css_selector("[role='button']")
    submit.click()


def main():
    parser = argparse.ArgumentParser(
        description='Automatic Google form filler.')
    parser.add_argument('url', help='full url of google form')
    parser.add_argument('-n', '--num', type=int, default=5,
                        help='number of repetitions')
    args = parser.parse_args()
    for _ in range(args.num):
        driver.get(args.url)
        fill_form(driver)
    driver.quit()


if __name__ == '__main__':
    main()
