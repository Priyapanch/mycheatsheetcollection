Perfect – let’s go deep into Step 3 (Test Case Layer creation) since that’s where most people get lost in UiPath testing.


---

🔹 Step 3: Creating Test Cases in UiPath

In UiPath Test Automation Project, a Test Case is just a special Sequence/Workflow marked as a test case. It can call your business flow (Flowchart) and pass parameters from test data.


---

✅ 3.1 Where Test Cases Fit

Libraries → hold your reusable “building blocks” (Login, Menu Select, etc.)

BusinessFlows (Flowcharts) → model the end-to-end processes (Approve, Reject, Cancel).

Test Cases (Sequences) → represent individual test variations of those flows, parameterized with test data.


Think of it like this:

TC_Approve_Confirm.xaml → runs ApproveFlow.xaml with DecisionType = Confirm
TC_Approve_Cancel.xaml → runs ApproveFlow.xaml with DecisionType = Cancel

So you don’t duplicate logic – you just reuse the flow and inject test data.


---

✅ 3.2 Steps to Create a Test Case in UiPath Studio

1. In your TestCases folder → Right-click → New → Test Case

Choose Sequence (simpler than Flowchart for test cases).

Name it TC_Approve_Confirm.



2. Inside that Test Case, use Invoke Workflow File:

Point it to BusinessFlows/ApproveFlow.xaml.

Pass arguments like:

in_DecisionType = "Confirm"

in_TestDataRow = CurrentRow (if you’re looping test data).




3. Add Assertions (Verify) where required:

Use Verify Expression activity:

Example: out_TotalTransactions = expectedTotal

This makes the test case fail/pass properly in Test Manager/Orchestrator.




4. Use Test Data Input:

From Excel/CSV → read row into a DataTable.

Loop over rows → pass row to Test Case.

Each row = a test execution instance.





---

✅ 3.3 Example Test Case (Approve Confirm)

TC_Approve_Confirm.xaml (Sequence)

1. Read Test Data Row (username, password, claim ID, decision type).


2. Invoke ApproveFlow.xaml with args:

in_Username = row("Username")

in_Password = row("Password")

in_ClaimID = row("ClaimID")

in_DecisionType = "Confirm"

out_TotalTransactions → varTotal



3. Verify Expression:

Expression: varTotal = row("ExpectedTotal")

On Fail: Mark as failed in Test Results.



4. Log Message: “TC_Approve_Confirm executed with result: Passed/Failed”.




---

✅ 3.4 Mapping Your Flows to Test Cases

Approve Flow → 2 Test Cases

TC_Approve_Confirm

TC_Approve_Cancel


Reject Flow → 2 Test Cases

TC_Reject_Confirm

TC_Reject_Cancel


Cancel Flow → 2 Test Cases

TC_Cancel_Confirm

TC_Cancel_Cancel



So 6 test cases total, but all reuse the same 3 business flows.


---

✅ 3.5 Why Test Case Layer is Critical

Keeps flows generic → ApproveFlow doesn’t hardcode “Confirm” vs “Cancel”.

Keeps test cases light → just data + asserts.

Integrates with Test Manager/Jira → each Test Case maps to a Jira story/test ID.

Easier reporting → Pass/Fail comes from Verify Expression, not just logs.



---

💡 Pro Tip for POC:
If you’re short on time, create one flow (ApproveFlow), two test cases (Confirm, Cancel), and show how data drives results. Then say “the same approach scales to Reject/Cancel flows.” That’s enough to prove the framework design.


---

Would you like me to also show you a mini UiPath workflow snippet (like pseudo-XAML with activities) of how TC_Approve_Confirm calls ApproveFlow with arguments and assertions? That way you can almost copy-paste into UiPath Studio for your POC.

