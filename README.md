# Automation Tools for Courses

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
11. Generate `.epub` file for Amazon Kindle using [Pandoc](https://pandoc.org) `pandoc --from gfm+task_lists --to epub3 README.md --output AB123_v1.2.3.epub --epub-cover-image=images/ebook.jpg --metadata title="⬆️ Abcda Befghi AB-123 (Abcda Befghi Something) Practice Tests Exams Questions & Answers" --metadata author="Daniel Danielecki" --toc --number-sections --shift-heading-level-by=-2`. Remember to change link `**[⬆ Back to Top](#table-of-contents)**` to the first question, and leave only questions in the Markdown file.
12. Scale up image logo for promotional image above `1102x1102` using https://bigjpg.com.
13. Scale down image logo for promotional image to `1102x1102` and replace logo layer in GIMP file, use such promotional image.
14. For eBook, keep promotional image in `1102x1102`.

Notes:
- `readme.py` doesn't returns the last question, needs to be added manually or fixed
