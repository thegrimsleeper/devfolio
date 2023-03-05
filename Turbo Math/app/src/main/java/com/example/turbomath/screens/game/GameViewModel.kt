package com.example.turbomath.screens.game

import android.os.CountDownTimer
import android.text.format.DateUtils
import android.util.Log
import android.view.View
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.Transformations
import androidx.lifecycle.ViewModel

class GameViewModel: ViewModel() {
    private val PROBLEM_NUM_RANGE_ONE = (1..10)
    private val PROBLEM_NUM_RANGE_TWO = (3..17)
    private val PROBLEM_NUM_RANGE_THREE = (7..26)
    private val ADJUSTMENT_ANSWER_RANGE = (2..4)

    // Code copied from GuessIt; companion code for timer
    companion object {
        // These represent different important times
        // This is when the game is over
        const val DONE = 0L
        // This is the number of milliseconds in a second
        const val ONE_SECOND = 1000L
        // This is the total time of the game
        const val COUNTDOWN_TIME = 3000L
    }

    // Create a timer
    private val timer : CountDownTimer

    // Current Score
    private val _score = MutableLiveData<Int>()
    val score: LiveData<Int>
        get() = _score

    // Current Problem
    private val _mathProblem = MutableLiveData<String>()
    val mathProblem: LiveData<String>
        get() = _mathProblem

    // Left answer holder
    private val _leftAnswer = MutableLiveData<String>()
    val leftAnswer: LiveData<String>
        get() = _leftAnswer

    // Right answer holder
    private val _rightAnswer = MutableLiveData<String>()
    val rightAnswer: LiveData<String>
        get() = _rightAnswer

    // Progress Bar View current progress
    private val _progressBarStatus = MutableLiveData<Int>()
    val progressBarStatus: LiveData<Int>
        get() = _progressBarStatus

    // Game Finished bool
    private val _gameOver = MutableLiveData<Boolean>()
    val gameOver: LiveData<Boolean>
        get() = _gameOver

    // Variables for ViewModel calculations only; not shared/observed elsewhere
    private var operator: Char = '='
    private var leftNumber: Int = 0
    private var rightNumber: Int = 0
    private var correctAnswer: Int = 0
    private var wrongAnswer: Int = 0
    private var progressTicker: Int = 0

    // On ViewModel init; set variables, create problem, create & start timer
    init {
        _gameOver.value = false
        _score.value = 0
        newProblem()

        // Create timer object; triggers game over at 0
        timer = object : CountDownTimer(COUNTDOWN_TIME, ONE_SECOND) {
            override fun onTick(millisUntilFinished: Long) {
                _progressBarStatus.value = (progressTicker*100/(COUNTDOWN_TIME/ONE_SECOND)).toInt()
                progressTicker += 1
            }
            override fun onFinish() {
                _gameOver.value = true
            }
        }
        timer.start()
    }

    // Override the onCleared to ensure timer is canceled
    override fun onCleared() {
        super.onCleared()
        timer.cancel()
    }

    // Get a Math problem
    private fun getProblem(): String {
        operator = getOperator()
        rightNumber = getNumber()
        if (operator == '-') {
            while (leftNumber < rightNumber ){
                leftNumber = getNumber()
            } // prevent subtraction where answer would be 0
            if (leftNumber == rightNumber) {
                rightNumber -= 1
            }
        }
        else {
            leftNumber = getNumber()
        }
        return "${leftNumber.toString()} $operator ${rightNumber.toString()}"
    }

    // Randomly choose operator for mathProblem
    private fun getOperator(): Char {
        return when {
            _score.value!! <= 5 -> '+'
            else -> {
                return when ((1..2).random()) {
                    1 -> '+'
                    else -> '-'
                }
            }
        }
    }

    // Assign numbers to left/right of mathProblem based on score
    private fun getNumber(): Int {
        return when {
            _score.value!! <= 5 -> PROBLEM_NUM_RANGE_ONE.random()
            _score.value!! <= 15 -> PROBLEM_NUM_RANGE_TWO.random()
            _score.value!! <= 30 -> {
                if (operator == '-') {
                    PROBLEM_NUM_RANGE_TWO.random()
                } else {
                    (PROBLEM_NUM_RANGE_THREE).random()
                }
            }
            else -> (PROBLEM_NUM_RANGE_THREE).random()
        }
    }

    // Calculate Correct Answer
    private fun getCorrectAnswer(): Int {
        return when (operator) {
            '+' -> (leftNumber + rightNumber)
            '-' -> (leftNumber - rightNumber)
            else -> 42069 // how the fuck did you get here?
        }
    }

    // Generate an Incorrect Answer : can be simplified need to review
    private fun getWrongAnswer(): Int {
        val adjustValue = (ADJUSTMENT_ANSWER_RANGE).random()
        return when ((1..2).random()) {
            1 -> correctAnswer + adjustValue
            else -> {
                if (correctAnswer - adjustValue > 0) {
                    correctAnswer - adjustValue
                } else {
                    correctAnswer + adjustValue
                }
            }

        }
    }

    // call necessary functions to get new problem, answers, and assign them to buttons
    private fun newProblem() {
        _mathProblem.value = getProblem()
        correctAnswer = getCorrectAnswer()
        wrongAnswer = getWrongAnswer()
        shuffleAnswers()
    }

    // Shuffle Answers to new variables to assign to buttons
    private fun shuffleAnswers() {
        when ((1..2).random()) {
            1 -> {
                _leftAnswer.value = correctAnswer.toString()
                _rightAnswer.value = wrongAnswer.toString()
            }
            else -> {
                _leftAnswer.value = wrongAnswer.toString()
                _rightAnswer.value = correctAnswer.toString()
            }
        }
    }

    // called when answer is selected; check if correct/incorrect
    fun checkCorrectClick(ans: String) {
        if (correctAnswer == ans.toInt()) {
            _score.value = _score.value?.plus(1)
            newProblem()
            timer.cancel()
            progressTicker = 0

            timer.start()
        } else {
            _gameOver.value = true
        }
    }

    fun gameFinishedStateReset() {
        _gameOver.value = false
    }
}
