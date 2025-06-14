# Automation Tools for Courses

## Usage

Run them using `python3 sample_tool.py`. Of course, you need a `Python` (3). The imported libraries to these scripts will be need to be installed using `pip3 install <package_name>`.

Maintained scripts:

- `web-scrap-*.py`;
- `readme-*.py`;

## Course Publication Process

1. Scrap questions from `exam4training.com` using [web-scrap-exam4training.py](/web-scrap-exam4training.py).
2. Format questions to our `GitHub` format.
3. Scrap questions from `vceguide.com`, using [web-scrap-vce.py](/web-scrap-vce.py), add only non-repeated to questions.
4. Format questions to our `GitHub` format.
5. Add manually questions from `exam-answer.com`, add only non-repeated to questions keeping our `GitHub` format.
6. Manually check for questions on `examtopics.com` until middle of the exam, i.e., when there's a paywall, add only non-repeated to questions.
7. Manually copy/paste each question to Google and look for community discussions on `examtopics.com`, fix correct answer.
8. Generate Table of Contents automatically using [DocToc](https://github.com/thlorenz/doctoc).
9. Number Table of Contents using [Regex Text Generator](https://marketplace.visualstudio.com/items?itemName=rioj7.regex-text-gen) as explained in [search and replace with regex to increment numbers in Visual Studio Code](https://stackoverflow.com/questions/58392686/search-and-replace-with-regex-to-increment-numbers-in-visual-studio-code), the only 1 difference is our generator expression is `{{=i+1}}` instead of `{{=N[1]+1}}`.
10. Scale up image logo for promotional image above `1102x1102` using [Bigjpg](https://bigjpg.com).
11. Scale down image logo for promotional image to `1102x1102` and replace logo layer in a GIMP files (locally stored) for ebooks/courses, use such promotional image.
12. Remove typos using `Amazon Kindle Direct Publishing` automatic proofreading software.
13. Publish on `GitHub` with the generated Table of Contents.
14. Release course on `GitHub`.
15. Add repo URL to the released course on `GitHub` to [our platform's repo exams.json file](https://github.com/Ditectrev/Practice-Exams-Platform/blob/main/lib/exams.json).
16. Course will be automatically build, deployed & published on [our platform](https://education.ditectrev.com).
17. Prepare `Udemy` format using [readme-udemy.py](/readme-udemy.py). Images needs to be uploaded manually, and some minor bugs required to be solved manually almost always occur during the process.
18. Publish the course on `Udemy`.
19. Generate `.pdf` format using Visual Studio Code's extension [Markdown PDF](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf), only `# COURSE TITLE`, promotional image & content from below `## Table of Contents` stays. Everything else must be removed before generating a `.pdf`. After that, the document is ready to generation the `.pdf` with questions to answers. For books, remove also the line, which creates contents of links at the end of the document, i.e., `[^X]:[CodeSandbox: ...]` (see https://github.com/yzane/vscode-markdown-pdf/pull/351 & https://github.com/yzane/vscode-markdown-pdf/issues/181).
20. Generate `.pdf` without answers by simply replacing `- [x]` to `- [ ]`.
21. Prepare to generate for `.epub` format by: 1. Change link `**[⬆ Back to Top](#table-of-contents)**` to the first question. 2. Remove `# COURSE TITLE` and `## Table of Contents` as well, leave only questions in the Markdown file. 3. Use `**` for correct answers (`CMD/CTRL` + `D` on `- [x]`, `View` -> `Word Wrap`, and incorporate these changes automatically). 4. The entire correct answer should be around `**`, e.g., `- [x] **This is correct answer for EPUB format.**`. 5. After that, the document is ready to generation the `.epub` with questions to answers. For books, change the line, which links to contents of links at the end of the document, i.e., `[^X]CodeSandbox: ...]` to `[CodeSandbox: CODESANDBOX_TITLE](LINK_TO_PREVIEW) (URL link to rewrite in the browser for printed version: [LINK_TO_PREVIEW](LINK_TO_PREVIEW)), last access: DATE.`.
22. Generate `.epub` format using [Pandoc](https://pandoc.org): `pandoc --from gfm+task_lists --to epub3 README.md --output AB123_v1.2.3.epub --epub-cover-image=images/ebook.jpg --metadata title="⬆️ Abcda Befghi AB-123 (Abcda Befghi Something) Practice Tests Exams Questions & Answers" --metadata author="Daniel Danielecki" --toc --number-sections --shift-heading-level-by=-2`.
23. Amazon for printing versions must be without ⬆️ and `**[⬆ Back to Top](#sample-link-to-first-question)**`.
24. Generate `.epub` without answers by simply replacing `- [x]` to `- [ ]`, and `- [x] **This is correct answer for EPUB format.**` with `- [ ] This is correct answer for EPUB format.`.
25. Publish the ebooks in `.epub`/`.pdf` formats to [Etsy](https://ditectrev.etsy.com), [Google Play Books](https://play.google.com/store/books/collection/cluster?gsr=SheCARQKEAoMc2UwRUVRQUFRQkFKEAkQBA%3D%3D:S:ANO1ljJWsUo), our [Shop](https://shop.ditectrev.com).
