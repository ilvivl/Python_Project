# Марковские цепи
## цепь 
1. Простая Марковская цепь, основное предположение в теореме Байеса для Марковский цепи, формула для нахождения распределения вероятностей по состояниям по имеющейся начальной вероятности и матрице переходов
2. Марковская цепь в определениях с википедии, где X - состояния, A - матрица переходов между скрытыми состояниями, B - матрица условных вероятностей P(наблюдение|состояние), а - распределение, O - наблюдения. Более полное объяснение терминологии (а на разных сайтах и даже на разных страницах вики оно разное) посмотри на странице по алгоритму Viterbi (следующий пункт) 
3. Алгоритм Viterbi с объяснением динамического программирования там использованного
Ссылки: https://en.m.wikipedia.org/wiki/Viterbi_algorithm. Просто упомяни про оценку точности 
4. Forward- backward алгоритм с объяснением теорвера там используемого
Ссылки: https://en.m.wikipedia.org/wiki/Forward–backward_algorithm
5. Алгоритм Baum-Welch его начинай писать только после Forward- backward
6. В файле analysis/markov_chain/Viterbi_try.py я примерно описал как данный алгоритм наложить на нашу задачу. Объяснение того почему именно этот, а никакой другой я напишу самостоятельно 
7. Для оценки метрик мы будем использовать ROC-AUG, базовые понятия напиши, сам алгоритм можешь не писать, так как мы возьмём этот алгоритм из sklearn.