Here’s a **clear, practical guide** to looping through **HTML web table pagination and collecting data in Robot Framework** — this is a *very common real-world automation task*, so you’re asking the right thing 👍

I’ll show:

1. **Concept**
2. **Required libraries**
3. **Basic pagination loop**
4. **Extracting table data**
5. **Full working example**
6. **Common pitfalls & best practices**

---

## 🧠 Core Idea

In **Robot Framework**, pagination scraping works like this:

1. Open the page
2. Read all rows from the current table
3. Store the data
4. Click **Next page**
5. Repeat until:

   * “Next” button is disabled, OR
   * Page number reaches max

---

## 📦 Required Libraries

Most web table pagination is done using **SeleniumLibrary**.

```robot
Library    SeleniumLibrary
Library    Collections
```

---

## 🔍 Typical HTML Pagination Structure

Usually looks like:

* A **table** (`<table><tr><td>`)
* A **Next** button:

  * `<a>` or `<button>`
  * Disabled on last page

Example:

```html
<button class="next disabled">Next</button>
```

---

## 🔁 Strategy Options

### Option 1 – Loop Until "Next" Is Disabled (Best)

✔ Works even when page count changes

### Option 2 – Loop Using Page Numbers

✔ Simpler, but brittle if pagination changes

---

## 🧪 Example Website Assumption

* Table rows: `//table/tbody/tr`
* Columns: `td[1]`, `td[2]`, `td[3]`
* Next button: `//button[@id="next"]`

---

## 🧩 Basic Pagination Loop

```robot
WHILE    ${True}
    Collect Table Data
    Exit For Loop If    ${IS_LAST_PAGE}
    Click Next Page
END
```

---

## 🧩 Keyword: Collect Table Data

```robot
Collect Table Data
    ${rows}=    Get Element Count    //table/tbody/tr

    FOR    ${i}    IN RANGE    1    ${rows}+1
        ${col1}=    Get Text    //table/tbody/tr[${i}]/td[1]
        ${col2}=    Get Text    //table/tbody/tr[${i}]/td[2]
        ${col3}=    Get Text    //table/tbody/tr[${i}]/td[3]

        Log    ${col1} | ${col2} | ${col3}
    END
```

---

## 🧩 Keyword: Detect Last Page

```robot
Check If Last Page
    ${disabled}=    Run Keyword And Return Status
    ...    Element Should Be Disabled    //button[@id="next"]
    [Return]    ${disabled}
```

---

## 🧩 Keyword: Click Next Page

```robot
Click Next Page
    Click Element    //button[@id="next"]
    Wait Until Page Contains Element    //table/tbody/tr
```

---

## 🧩 Full Working Test Case Example

```robot
*** Settings ***
Library    SeleniumLibrary
Library    Collections

*** Variables ***
${URL}    https://example.com/table

*** Test Cases ***
Collect All Table Pages
    Open Browser    ${URL}    chrome
    Maximize Browser Window

    WHILE    ${True}
        Collect Table Data
        ${IS_LAST}=    Check If Last Page
        Exit For Loop If    ${IS_LAST}
        Click Next Page
    END

    Close Browser
```

---

## 🧠 Alternative: Loop by Page Number

If pages are numbered:

```robot
FOR    ${page}    IN RANGE    1    6
    Click Element    //a[text()='${page}']
    Wait Until Page Contains Element    //table/tbody/tr
    Collect Table Data
END
```

⚠️ Less flexible if total pages change.

---

## 📂 Saving Data (CSV Example)

```robot
Append To File    data.csv    ${col1},${col2},${col3}\n
```

Or use `Create List` + `Append To List` for structured data.

---

## ⚠️ Common Mistakes (Important)

❌ Not waiting after clicking Next
❌ Hardcoding sleep instead of waits
❌ Not checking disabled state
❌ Using absolute XPath when DOM changes

---

## ✅ Best Practices

✔ Use **Wait Until Element Is Visible**
✔ Prefer **relative XPath or CSS selectors**
✔ Store data in lists or dictionaries
✔ Log page numbers while looping
✔ Handle stale elements on page change

---

## 🚀 Want a Tailored Example?

If you want, I can:

* Adapt this to **your exact website**
* Handle **AJAX-loaded tables**
* Export to **Excel / CSV**
* Use **page numbers or infinite scroll**

Just tell me:
📌 Table HTML snippet or URL
📌 Pagination type
📌 Output format

I’ll customize it cleanly for you 😄
