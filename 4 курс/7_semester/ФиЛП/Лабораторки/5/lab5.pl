:-dynamic horse_position/2.

% проверка на выход за пределы шахматной доски
check_board(X, Y) :- X > 0, X < 9,
    Y > 0, Y < 9.


% Шаг вверх влево ↑↑←
move_horse(X, Y) :- NewX is X - 1, NewY is Y + 2,
	check_board(NewX, NewY),
	not(horse_position(NewX, NewY)),
	format("↑↑←~nШаг вверх влево.~nНовая позиция (~w,~w)~n", [NewX, NewY]),
    assert(horse_position(NewX, NewY)).
    
% Шаг вверх вправо ↑↑→
move_horse(X, Y) :- NewX is X + 1, NewY is Y + 2,
	check_board(NewX, NewY),
	not(horse_position(NewX, NewY)),
	format("↑↑→~nШаг вверх вправо.~nНовая позиция (~w,~w)~n", [NewX, NewY]),
    assert(horse_position(NewX, NewY)).
    
% Шаг вправо вверх →→↑
move_horse(X, Y) :- NewX is X + 2, NewY is Y + 1,
	check_board(NewX, NewY), 
	not(horse_position(NewX, NewY)),
	format("→→↑~nШаг вправо вверх.~nНовая позиция (~w,~w)~n", [NewX, NewY]),
    assert(horse_position(NewX, NewY)).

% Шаг вправо вниз →→↓
move_horse(X, Y) :- NewX is X + 2, NewY is Y - 1,
	check_board(NewX, NewY),
	not(horse_position(NewX, NewY)),
	format("→→↓~nШаг вправо вниз.~nНовая позиция (~w,~w)~n", [NewX, NewY]),
    assert(horse_position(NewX, NewY)).
    
% Шаг вниз вправо ↓↓→
move_horse(X, Y) :- NewX is X + 1, NewY is Y - 2,
	check_board(NewX, NewY),
	not(horse_position(NewX, NewY)),
	format("↓↓→~nШаг вниз вправо.~nНовая позиция (~w,~w)~n", [NewX, NewY]),
    assert(horse_position(NewX, NewY)).

% Шаг вниз влево ↓↓←
move_horse(X, Y) :- NewX is X - 1, NewY is Y - 2,
	check_board(NewX, NewY),
	not(horse_position(NewX, NewY)),
	format("↓↓←~nШаг вниз влево.~nНовая позиция (~w,~w)~n", [NewX, NewY]),
    assert(horse_position(NewX, NewY)).
    
% Шаг влево вниз ←←↓
move_horse(X, Y) :- NewX is X - 2, NewY is Y - 1,
	check_board(NewX, NewY),
	not(horse_position(NewX, NewY)),
	format("←←↓~nШаг влево вниз.~nНовая позиция (~w,~w)~n", [NewX, NewY]),
    assert(horse_position(NewX, NewY)).

% Шаг влево вверх ←←↑
move_horse(X, Y) :- NewX is X - 2, NewY is Y + 1,
	check_board(NewX, NewY),
	not(horse_position(NewX, NewY)),
	format("←←↑~nШаг влево вверх.~nНовая позиция (~w,~w)~n", [NewX, NewY]),
    assert(horse_position(NewX, NewY)).
    
    
horse_movement(X, Y) :-
	format("~nНовый мув~n"),
	move_horse(X, Y).
% ↑
% ←
% →
% ↓  
generate_3movements_horse(FirstX, FirstY) :-
	format("~nНачальная позиция (~w,~w)~n", [FirstX, FirstY]),
	check_board(FirstX, FirstY),
	assert(horse_position(FirstX, FirstY)),

	% Расчёт первого хода
	format("~nПервый ход:~n"),
	move_horse(FirstX, FirstY);

	% Расчёт второго хода
	format("~nВторой ход:~n"),
	horse_position(SecondX, SecondY),
	horse_movement(SecondX, SecondY);

	% Расчёт третьего хода
	format("~nТретий ход:~n"),
	horse_position(ThirdX, ThirdY),
	horse_movement(ThirdX, ThirdY).
	
% test: generate_3movements_horse(7, 1).
