# TelegramNLP
##Transformers
Transformers (Attention is all you need) were introduced in the context of machine translation with the purpose to avoid recursion in order to allow parallel computation (to reduce training time) and also to reduce drops in performance due to long dependencies. The main characteristics are:

Non sequential: sentences are processed as a whole rather than word by word.
Self Attention: this is the newly introduced 'unit' used to compute similarity scores between words in a sentence.
Positional embeddings: another innovation introduced to replace recurrence. The idea is to use fixed or learned weights which encode information related to a specific position of a token in a sentence.
The first point is the main reason why transformer do not suffer from long dependency issues. The original transformers do not rely on past hidden states to capture dependencies with previous words. They instead process a sentence as a whole. That is why there is no risk to lose (or "forget") past information. Moreover, multi-head attention and positional embeddings both provide information about the relationship between different words.

##RNN / LSTM
Recurrent neural networks and Long-short term memory models, for what concerns this question, are almost identical in their core properties:

Sequential processing: sentences must be processed word by word.
Past information retained through past hidden states: sequence to sequence models follow the Markov property: each state is assumed to be dependent only on the previously seen state.
The first property is the reason why RNN and LSTM can't be trained in parallel. In order to encode the second word in a sentence I need the previously computed hidden states of the first word, therefore I need to compute that first. The second property is a bit more subtle, but not hard to grasp conceptually. Information in RNN and LSTM are retained thanks to previously computed hidden states. The point is that the encoding of a specific word is retained only for the next time step, which means that the encoding of a word strongly affects only the representation of the next word, so its influence is quickly lost after a few time steps. LSTM (and also GruRNN) can boost a bit the dependency range they can learn thanks to a deeper processing of the hidden states through specific units (which comes with an increased number of parameters to train) but nevertheless the problem is inherently related to recursion. Another way in which people mitigated this problem is to use bi-directional models. These encode the same sentence from the start to end, and from the end to the start, allowing words at the end of a sentence to have stronger influence in the creation of the hidden representation. However, this is just a workaround rather than a real solution for very long dependencies.

