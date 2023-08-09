# Python Automation Markdown to Udemy Practice Test Batch Questions Uploader

## Process

1. Scrap questions from `exam-answer.com`.
2. Scrap questions from `exam4training.com`, add only non-repeated to questions.
3. Format questions to `Udemy` format.
4. Manually check for questions on `examtopics.com` until middle of the exam, i.e., when there's a paywall, add only non-repeated to questions, format it to `Udemy` format.
5. Manually copy/paste each question to Google and look for community discussions on `examtopics.com`, fix correct answer.
6. Publish a course.
7. Generate Table of Contents automatically using https://github.com/thlorenz/doctoc.
8. Number Table of Contents using https://marketplace.visualstudio.com/items?itemName=rioj7.regex-text-gen as explained in https://stackoverflow.com/questions/58392686/search-and-replace-with-regex-to-increment-numbers-in-visual-studio-code, the only 1 difference is our generator expression is `{{=i+1}}` instead of `{{=N[1]+1}}`.
9. Update `GitHub` with latest generated Table of Contents.
10. Publish on `Etsy`.

Notes:
- `readme.py` doesn't returns the last question, needs to be added manually or fixed
