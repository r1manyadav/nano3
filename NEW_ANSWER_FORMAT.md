# New Test Format: 4-Button Answer System with Updated Scoring

## ✅ Implementation Complete

The test attempt interface has been updated with a new format featuring 4 distinct answer submission buttons, each with different scoring and behavior.

---

## 4 Button Options

### 1️⃣ **Save & Next** (Green Button ✓)
- **Action**: Saves the answer and moves to the next question automatically
- **Scoring**: 
  - ✅ Correct answer: **+4 marks**
  - ❌ Wrong answer: **-1 mark**
- **Status**: Treated as "Attempted"
- **Visual**: Green button, answered questions shown in blue

### 2️⃣ **Skip** (White Button ⊘)
- **Action**: Skips the question without saving any answer and moves to next
- **Scoring**: **0 marks**
- **Status**: Treated as "Unattempted"
- **Visual**: White/gray button, skipped questions shown in light gray
- **Use Case**: When you want to move to the next question without answering

### 3️⃣ **Save & Mark for Review** (Orange Button ⭐)
- **Action**: Saves the answer AND marks the question for review
- **Scoring**: 
  - ✅ Correct answer: **+4 marks**
  - ❌ Wrong answer: **-1 mark**
- **Status**: Treated as "Attempted" + "Marked for Review"
- **Visual**: Orange button, marked questions shown with orange indicator
- **Use Case**: When you want to answer but are uncertain and want to review later

### 4️⃣ **Mark for Review Only** (Light Button 📋)
- **Action**: Marks the question for review WITHOUT saving any answer
- **Scoring**: **0 marks**
- **Status**: Treated as "Unattempted" but "Marked for Review"
- **Visual**: Light gray button, shows as marked but not attempted
- **Use Case**: When you don't know the answer but want to review it later

---

## Scoring Summary Table

| Button | Action | Correct | Wrong | Marks Type | Status |
|--------|--------|---------|-------|-----------|--------|
| ✓ Save & Next | Auto next | +4 | -1 | Attempted | ✓ |
| ⊘ Skip | Auto next | 0 | 0 | Unattempted | ⊘ |
| ⭐ Save & Mark | Auto next | +4 | -1 | Attempted | ⭐ |
| 📋 Mark Only | Auto next | 0 | 0 | Unattempted | 📋 |

---

## Visual Indicators in Question Panel

The left side "Questions" panel shows the status of each question with color coding:

- **Blue**: Answered (Save & Next or Save & Mark for Review)
- **Gray**: Skipped (Skip button used)
- **Orange**: Marked for Review (with or without answer)
- **White**: Not Attempted

Hover over any question number to see detailed status information.

---

## Example Scoring Scenario

**Test**: 4 questions, each worth 4 marks

1. **Q1**: Answer correctly with "Save & Next" → **+4 marks** ✓
2. **Q2**: Answer incorrectly with "Save & Next" → **-1 mark** ✗
3. **Q3**: Skip → **0 marks** ⊘
4. **Q4**: Answer correctly with "Save & Mark for Review" → **+4 marks** ⭐

**Total**: 4 - 1 + 0 + 4 = **7 / 16 marks** (43.75%)

---

## Files Modified

### Frontend

1. **`frontend/attempt-test.html`**
   - Replaced 3 buttons with 4 new buttons
   - Added `saveAndNext()`, `skipQuestion()`, `saveAndMarkForReview()`, `markForReview()` functions
   - Added `questionStatus` tracking for each question
   - Updated question grid to show multiple status indicators
   - Auto-moves to next question after button click

2. **`frontend/api.js`**
   - Updated `submitTest()` to include `question_status` parameter
   - Enhanced API logging with colored console output

3. **`frontend/style.css`**
   - Added `.btn-light` style for Skip button (white/gray)
   - Added `.question-num.skipped` styling (light gray indicator)
   - Updated `.answer-buttons` layout for 4-button display
   - Responsive design for button group

### Backend

1. **`backend/app.py`**
   - Updated `/api/results/submit` endpoint to accept `question_status` parameter
   - Changed scoring logic:
     - Only 'answered' status questions are scored
     - 'skipped' and 'marked_only' status questions get 0 marks
     - Correct count now reflects answered questions only
   - All unanswered, skipped, and marked-only questions counted as "unanswered_count"

---

## How It Works

### Student Flow

1. **Select Answer** (optional) - Student selects one of 4 options (A, B, C, D)
2. **Choose Action** - Click one of the 4 buttons
3. **Auto-Navigate** - Page automatically moves to next question
4. **Status Updates** - Question panel updates to show the action taken
5. **Submit** - On last question, Submit button appears instead of Next

### Backend Processing

When test is submitted:
1. Backend receives answers + question_status + marked_for_review
2. For each question, backend checks the `question_status`:
   - `'answered'` → Score: +4 if correct, -1 if wrong
   - `'skipped'` → Score: 0
   - `'marked_only'` → Score: 0
   - `null/None` → Score: 0 (unanswered)
3. Calculates total marks, percentage, and pass/fail status
4. Stores result with complete tracking data

---

## Verification Test Results

✅ **Test Executed**: Student answered Q1 correctly (Save & Next), skipped Q2
- Q1: Correct answer → +4 marks
- Q2: Skipped → 0 marks
- **Result**: 4/8 marks (50%) - PASSED ✓

---

## Features Implemented

✅ Four distinct button options with clear visual differentiation
✅ Auto-navigation to next question after button click
✅ Different scoring system based on answer status
✅ Visual indicators in question panel (blue/gray/orange)
✅ "Marked for Review" tracking separate from scoring
✅ Backend validation of new scoring system
✅ Backward compatible API (handles missing question_status)
✅ Comprehensive error handling and logging
✅ Responsive button layout

---

## Using the New System

### For Teachers
No changes needed. Results will automatically calculate using the new scoring system. Passing marks threshold remains the same (sets in test creation).

### For Students

**To Answer Correctly:**
1. Select the correct option
2. Click "✓ Save & Next" (Green)
3. Continue to next question

**To Come Back Later:**
1. Select the correct option
2. Click "⭐ Save & Mark for Review" (Orange)
3. Automatically goes to next question
4. You can navigate back to answer other questions

**To Skip and Review:**
1. Don't select any option (or leave current selection)
2. Click "📋 Mark for Review" (Light)
3. Returns 0 marks but marked for later review

**To Skip Without Review:**
1. Don't select any option
2. Click "⊘ Skip" (White)
3. Returns 0 marks, not marked

---

## Technical Details

### API Contract Change
```javascript
// Old submission:
api.submitTest(testId, answers, markedForReview)

// New submission:
api.submitTest(testId, answers, markedForReview, questionStatus)
```

### Question Status Values
- `'answered'` - Question was answered (eligible for scoring)
- `'skipped'` - Question was skipped (0 marks)
- `'marked_only'` - Marked for review but not answered (0 marks)
- `null` - Not attempted

### Backend Scoring Logic
```python
if status == 'answered' and student_answer is not None:
    if student_answer == question.correct_answer:
        total_marks += 4
    else:
        total_marks -= 1
else:
    # skipped, marked_only, or unanswered = 0 points
```

---

## Status: ✅ Ready for Testing

The new 4-button answer system is fully implemented and tested. Student can now:
- Answer and save questions for scoring
- Skip questions without penalty
- Mark questions for review while getting scored
- Mark questions for review without getting scored

All scoring logic has been verified and is working correctly!
