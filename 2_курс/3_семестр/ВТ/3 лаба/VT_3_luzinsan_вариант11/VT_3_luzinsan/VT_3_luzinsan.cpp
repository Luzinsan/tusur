#include <iostream>

int main()
{
    __int8 C = -15;
    __int16 B = 257;
    __int32 A = -3000;
    __int32 D; // Результат выражения D = (B * C) + A
    __int32 E; // Результат выражения E = (B - C) / B - A
    std::cout << "\n\tInput:\tdec: A = " << A << ";\tB = " << static_cast<int>(B) << ";\tC = " << static_cast<int>(C);
    std::cout.unsetf(std::ios::dec);
    std::cout.setf(std::ios::hex);
    std::cout << "\n\t      \thex: A = " << A << ";\tB = " << static_cast<int>(B) << ";\tC = " << static_cast<int>(C);
    std::cout << "\n\t\tD = (B * C) + A\tE = (B - C)/ B - A";
    _asm
    {
       
        /*
        * Вычислить целочисленное выражение, указанное в варианте задания. При этом, и
        * операнды и результаты вычислений следует выводить как в десятичном,
        * так и в шестнадцатеричном виде.
        *
        11) A(dword), B(word), C(byte)
        Вычислить:
            D = (B * С) + A;
            E = (B - C) / B - A.
        */

        mov al, byte ptr C
        cbw
        imul B
        add ax, word ptr A
        adc dx, word ptr A + 2
        mov word ptr D, ax
        mov word ptr D + 2, dx
        
        mov ax, word ptr B 
        movsx dx, byte ptr C
        sub ax, dx
        cwd // ax -> (dx:ax)
        idiv B  // (dx:ax) / B
        cwde
        sub eax, A
        mov E, eax    
    }
    std::cout.unsetf(std::ios::hex);
    std::cout.setf(std::ios::dec);
    std::cout << "\n\tOutput: \ndec:\tD = " << D << ";\tE = " << E << '\n';
    std::cout.unsetf(std::ios::dec);
    std::cout.setf(std::ios::hex);
    std::cout << "\tOutput: \nhex:\tD = " << D << ";\tE = " << E << '\n';

    return 0;
}

