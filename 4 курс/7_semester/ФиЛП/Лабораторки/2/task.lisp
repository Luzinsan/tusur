; Вариант 1
; Определите функцию "трубопровод" (f s x), 
; где x - число, a s - список имен функций 
; (gl g2 g3 ... gn).
; Функция f должна вычислять значение gl(g2(g3(g4...gn(x)...))).

;gnu clisp  2.49.60
(defun add1 (x)
  (+ x 1))

(defun g1 (x) (* x 2))
(defun g2 (x) (+ x 3))
(defun g3 (x) (/ x 2))

(defun f (s x)
  (cond ((null s) x)
        (t (funcall (car s) (f (cdr s) x)))))

;add1(g1(g2(g3(1)))) => for 1 => ((1 / 2) + 3) * 2 + 1 = 8

(print "Обработанное число из трубопровода: ")
(let ((number (read)))
	(print (f '(add1 g1 g2 g3) number))
)




