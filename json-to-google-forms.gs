/**
 * Chaotic Group Chat Quiz Generator
 * ---------------------------------
 * This Google Apps Script builds a full Google Form quiz using 
 * anonymized group-chat messages. Each question presents a real 
 * message (>80 chars, chosen for chaotic or suggestive out-of-context 
 * energy), and the user must guess which friend said it.
 *
 * Features:
 * - Creates a new Google Form in quiz mode
 * - Imports question data from a JSON structure
 * - Adds multiple-choice answers with a correct option
 * - Assigns 1 point per question
 * - Supports any number of questions
 *
 * Data Pipeline:
 * 1. Export conversations from Facebook (JSON format)
 * 2. Run a Python script to anonymize all names
 * 3. Use ChatGPT to extract the most unhinged, >80-character messages
 * 4. Generate a JSON block with:
 *      { question: "...", options: [...], correct: "..." }
 * 5. Paste JSON into this script and execute to build the Google Form
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
