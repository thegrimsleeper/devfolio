package com.example.turbomath.screens.game

import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.databinding.DataBindingUtil
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import com.example.turbomath.R
import com.example.turbomath.databinding.FragmentGameBinding

class GameFragment : Fragment() {

    private lateinit var viewModel: GameViewModel

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val binding: FragmentGameBinding =
            DataBindingUtil.inflate(inflater, R.layout.fragment_game, container, false)

        // Get viewModel object using ViewModelProvider
        Log.i("GameFragment","Called ViewModelProvider and initialize gameviewmodel ")
        viewModel = ViewModelProvider(this).get(GameViewModel::class.java)

        // Bind viewModel object to the layout via binding
        binding.gameViewModel = viewModel
        binding.lifecycleOwner = this

        // Observe gameFinsihed state; true when timer hits 0
        viewModel.gameOver.observe(this, Observer { gameEnd ->
            if (gameEnd) {
                gameFinished()
                viewModel.gameFinishedStateReset()
            }
        })

        /*
        viewModel.problem.observe(this, Observer { mathProblem ->
            binding.gameMathProblem.text = mathProblem
        })
        */
        return binding.root
    }

    // Called when game is finished; when gameViewModel timer hits 0
    private fun gameFinished() {
        val finalScore = viewModel.score.value ?: 0
        findNavController().navigate(GameFragmentDirections.actionNavGameFragmentToNavScoreFragment(finalScore))
        // Toast.makeText(this.activity,"Game Over!", Toast.LENGTH_SHORT).show()
    }

}

