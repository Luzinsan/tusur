#include "QueueNode.h"
#include <iostream>
namespace luzinsan
{
	//Указатель на начальный элемент очереди
	QueueNode* QueueNode::q_BeginQueueA{ nullptr };
	QueueNode* QueueNode::q_BeginQueueA_B{ nullptr };
	QueueNode* QueueNode::q_BeginQueueB{ nullptr };
	//Указатель на конечный элемент очереди
	QueueNode* QueueNode::q_EndQueueA{ nullptr };
	QueueNode* QueueNode::q_EndQueueA_B{ nullptr };
	QueueNode* QueueNode::q_EndQueueB{ nullptr };
	int QueueNode::q_A{ 5 }, QueueNode::q_B{ 10 };


	QueueNode::QueueNode() : q_info{ 0 }, q_next{nullptr}{}
	
	const QueueNode& QueueNode::SetA(int A) { q_A = A; return *this; }
	const QueueNode& QueueNode::SetB(int B) { q_B = B; return *this; }

	// Добавить элемент в очередь
	const QueueNode& QueueNode::EnQueue(int x)
	{
		QueueNode* p = new QueueNode;
		if (p)
		{
			p->q_info = x;
			p->q_next = nullptr;

			if (x < q_A)
			{
				if (q_BeginQueueA == nullptr)
					q_BeginQueueA = p;
				else
					q_EndQueueA->q_next = p;
				q_EndQueueA = p;
			}
			else if (x >= q_A && x < q_B)
			{
				if (q_BeginQueueA_B == nullptr)
					q_BeginQueueA_B = p;
				else
					q_EndQueueA_B->q_next = p;
				q_EndQueueA_B = p;
			}
			else
			{
				if (q_BeginQueueB == nullptr)
					q_BeginQueueB = p;
				else
					q_EndQueueB->q_next = p;
				q_EndQueueB = p;
			}
		}
		else exit(EOF);
		return *this;
	}


	// Возвратить первый элемент очереди
	int QueueNode::DeQueue()
	{
		int val;
		QueueNode* p = new QueueNode;
		if (p)
		{
			p = q_BeginQueueA;
			if (q_BeginQueueA == nullptr)
			{
				p = q_BeginQueueA_B;
				if (q_BeginQueueA_B == nullptr)
				{
					p = q_BeginQueueB;
					if (q_BeginQueueB == nullptr)
					{
						std::cout << "\nОчередь закончилась\n";
						return 0;
					}
					else
					{
						val = q_BeginQueueB->q_info;
						q_BeginQueueB = p->q_next;
						if (q_BeginQueueB == nullptr)
							q_EndQueueB = nullptr;
					}
				}
				else
				{
					val = q_BeginQueueA_B->q_info;
					q_BeginQueueA_B = p->q_next;
					if (q_BeginQueueA_B == nullptr)
						q_EndQueueA_B = nullptr;
				}
			}
			else
			{
				val = q_BeginQueueA->q_info;
				q_BeginQueueA = p->q_next;
				if (q_BeginQueueA == nullptr)
					q_EndQueueA = nullptr;
			}
			delete p;
		}
		else exit(EOF);
		return val;
	}
}