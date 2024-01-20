#include <iostream>

int func(double    , int d);


int main()
{
    func(0.2, 3);
    return 0;
}

int func(double s, int d)
{
    std::cout << "success";
    return 0;
}
