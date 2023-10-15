% Генератор логического выражения.
/*
	Для заданного списка входных переменных 
	и заданной таблице истинности на основе заданных операций: 
	И, ИЛИ, НЕ. 
	
	Выражение сгенерировать с помощью поиска в дереве решений методом в ширину.
	
*/

% Операция И (AND)
and(true, true, true).
and(_, _, false).

% Операция ИЛИ (OR)
or(false, false, false).
or(_, _, true).

% Операция НЕ (NOT)
not(true, false).
not(false, true).

% Определение таблицы истинности для A и B
truth_table(A, B) :-
    member(A, [true, false]),
    member(B, [true, false]).

% Генерация выражения методом поиска в ширину
generate_expression(Expression) :-
    truth_table(A, B),
    generate_expression_bfs([A, B], Expression).

generate_expression_bfs([Result | _], Result) :-
    desired_truth_value(Result).

generate_expression_bfs([Current | Queue], Expression) :-
    extend_node(Current, ExtendedNodes),
    append(Queue, ExtendedNodes, NewQueue),
    generate_expression_bfs(NewQueue, Expression).

extend_node(Node, ExtendedNodes) :-
    (and(Node, NewNode) ; or(Node, NewNode) ; not(Node, NewNode)),
    ExtendedNodes = [NewNode | RestNodes],
    extend_node(RestNodes, ExtendedNodes).

desired_truth_value(Result) :-
    Result = true.

% Преобразование логического выражения в человекочитаемую строку
expression_to_string(true, 'true') :- !.
expression_to_string(false, 'false') :- !.
expression_to_string(and(X, Y), R) :-
    expression_to_string(X, Xs),
    expression_to_string(Y, Ys),
    atomic_list_concat(['(', Xs, ' и ', Ys, ')'], R).
expression_to_string(or(X, Y), R) :-
    expression_to_string(X, Xs),
    expression_to_string(Y, Ys),
    atomic_list_concat(['(', Xs, ' или ', Ys, ')'], R).
expression_to_string(not(X), R) :-
    expression_to_string(X, Xs),
    atomic_list_concat(['не ', Xs], R).

% Запуск генератора и получение выражения в виде строки
% generate_expression(Expression), expression_to_string(Expression, Result), writeln(Result).

