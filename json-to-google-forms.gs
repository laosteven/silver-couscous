/**
json-to-google-forms.gs

Purpose:
- Generates a Google Form quiz from a JSON object.

Input JSON format:
[
  {
    "question": "Long Facebook message",
    "options": ["Friend_A", "Friend_B", "Friend_C", "Friend_D"],
    "correct": "Friend_A"
  }
]

Usage:
1. Paste your JSON content in the `data` variable.
3. Run createQuizForm() in Google Apps Script.

Notes:
- Creates a multiple-choice quiz.
- Marks the correct answer automatically.
- Adds correct-answer feedback.
*/

function createQuizForm() {
  // === 1. YOUR JSON GOES HERE ===
  var data = [
    // ... your full 20-question JSON objects ...
  ];

  // === 2. CREATE THE FORM ===
  var form = FormApp.create("Chaotic Group Chat Quiz");
  form.setIsQuiz(true);

  // === 3. ADD QUESTIONS ===
  data.forEach(function(item) {
    var question = form.addMultipleChoiceItem();
    question.setTitle(item.question);
    
    // Create choices (mark correct one)
    var choices = item.options.map(function(opt) {
      return question.createChoice(opt, opt === item.correct);
    });
    question.setChoices(choices);
    question.setRequired(true);

    // === 4. SET POINTS TO 1 ===
    var feedback = FormApp.createFeedback().build(); // empty feedback
    var correctFeedback = FormApp.createFeedback().build();
    var itemSettings = question.asQuizItem();
    itemSettings.setPoints(1);
    itemSettings.setFeedbackForCorrect(correctFeedback);
    itemSettings.setFeedbackForIncorrect(feedback);
  });

  Logger.log("Form created: " + form.getEditUrl());
}
