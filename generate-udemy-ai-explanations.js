// Function to simulate clicking elements by selector
function clickElementBySelector(selector) {
  const element = document.querySelector(selector);
  if (element) {
    element.click();
    return true;
  } else {
    console.warn(`Element with selector '${selector}' not found.`);
    return false;
  }
}

// Function to simulate clicking elements by text
function clickElementByText(tag, text) {
  const elements = document.getElementsByTagName(tag);
  for (let element of elements) {
    if (element.textContent.trim() === text) {
      element.click();
      return true;
    }
  }
  console.warn(`Element with tag '${tag}' and text '${text}' not found.`);
  return false;
}

// Function to perform the sequence of actions
function performSequence() {
  const divSelector = '.left-area--item-wrapper--FMMrx';
  const divElements = document.querySelectorAll(divSelector);
  let index = 0;

  function clickNextDiv() {
    if (index >= divElements.length) {
      console.log('All div elements have been processed.');
      return;
    }

    divElements[index].click();

    setTimeout(() => {
      if (clickElementByText('button', 'Generate all answer explanations with AI')) {
        // Wait 15 seconds before clicking "Accept and edit" spans
        setTimeout(() => {
          const spanSelector = 'span';
          const spanText = 'Accept and edit';
          const saveText = 'Save question';

          // Click all "Accept and edit" spans
          const acceptAndEditSpans = document.querySelectorAll(`${spanSelector}`);
          for (let span of acceptAndEditSpans) {
            if (span.textContent.trim() === spanText) {
              span.click();
            }
          }

          // Click the "Save question" span
          setTimeout(() => {
            clickElementByText(spanSelector, saveText);

            // Move to the next div and repeat the process
            index++;
            setTimeout(clickNextDiv, 10000); // Adjust delay as necessary
          }, 10000); // Adjust delay as necessary
        }, 15000); // Wait 15 seconds before finding "Accept and edit" spans
      } else {
        console.log('Failed to click "Generate all answer explanations with AI" button.');
        index++;
        setTimeout(clickNextDiv, 1000); // Adjust delay as necessary
      }
    }, 500); // Adjust delay as necessary
  }

  // Start the sequence
  clickNextDiv();
}

// Start the process
performSequence();
