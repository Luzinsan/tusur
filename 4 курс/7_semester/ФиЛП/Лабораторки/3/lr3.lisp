;gnu clisp  2.49.60


; задание уравнения в виде списка
(setq meEquation '(A / x + B = C))

; выделение левой части относительно символа op
(defun left(e op)
    (if e
        (let ((f (car e)))
           (if (eq f op) nil
               (cons f (left (cdr e) op))
           )
        )
        nil
     )
)

; выделение правой части относительно символа op
(defun right(e op)
    (if e
        (let ((r (cdr e)))
            (if (eq (car e) op) r
                (right r op)
            )
        )
        nil
    )
)

; решение уравнения
(defun res(e)
    (let ((l (left e '=)))
        (if l
            (let ((c (first (right e '=)))
                  (b (first (right l '+)))
                  (a (first (left l '+)))
                  (varx (first (cddr (left l '+))))
                 )
            (if (and c a b varx)
                (format nil "~S = ( ~S - ~S ) / ~S" varx c b a) 
            nil
            )
            )
            nil
        )
    )
)

; вывод сообщения об ошибке при неправильно заданном уравнении
(defun res2(e)
    (let ((r (res e)))
        (if r r "Ошибка")
    )
)

; вывод результата решения
(print (res2 meEquation))

