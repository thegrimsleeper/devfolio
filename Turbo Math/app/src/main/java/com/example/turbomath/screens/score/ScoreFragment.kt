package com.example.turbomath.screens.score

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import androidx.navigation.fragment.navArgs
import com.example.turbomath.R
import com.example.turbomath.databinding.FragmentScoreBinding

class ScoreFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val binding: FragmentScoreBinding =
            DataBindingUtil.inflate(inflater, R.layout.fragment_score, container, false)

        // Get args using by navArgs property delegate
        val scoreArgs = ScoreFragmentArgs.fromBundle(requireArguments())
        // vs. https://stackoverflow.com/questions/57034392/what-is-the-difference-between-by-navargsscorefragmentargs-vs-scorefragme
        // val scoreFragmentArgs by navArgs<ScoreFragmentArgs>()

        val viewModelFactory = ScoreViewModelFactory(scoreArgs.score)
        val viewModel = ViewModelProvider(this, viewModelFactory).get(ScoreViewModel::class.java)

        binding.scoreViewModel = viewModel
        binding.lifecycleOwner = this


        viewModel.playAgain.observe(this, Observer { againState ->
            if (againState) {
                findNavController().navigate(ScoreFragmentDirections.actionNavScoreFragmentToNavGameFragment())
                viewModel.toPlayAgainStateReset()
            }
        })

        return binding.root
    }


}