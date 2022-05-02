package com.example.turbomath.screens.score

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class ScoreViewModel(finalScore: Int) : ViewModel() {

    private val _score = MutableLiveData<Int>()
    val score: LiveData<Int>
        get() = _score

    private val _playAgain = MutableLiveData<Boolean>()
    val playAgain: LiveData<Boolean>
        get() = _playAgain

    private val _congrats = MutableLiveData<String>()
    val congrats: LiveData<String>
        get() = _congrats

    private val congratsWords = listOf<String>(
        "Amazing",
        "Astonishing",
        "Incredible",
        "Impressive",
        "Terrific",
        "Tremendous")

    init {
        _score.value = finalScore
        _congrats.value = chooseCongrats()
    }

    private fun chooseCongrats(): String {
         return congratsWords[((1 until congratsWords.size).random() - 1)]
    }

    fun toPlayAgain() {
        _playAgain.value = true
    }

    fun toPlayAgainStateReset() {
        _playAgain.value = false
    }
}