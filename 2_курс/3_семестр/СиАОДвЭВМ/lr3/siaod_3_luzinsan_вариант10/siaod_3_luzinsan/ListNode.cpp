#include "ListNode.h"
#include <iostream>
#include <cassert> 
namespace luzinsan
{
	ListNode* ListNode::BeginList{nullptr}; 
	ListNode*& ListNode::getBeginList() { return BeginList; }
	ListNode*& ListNode::getNext() { return l_next; }
	ListNode::ListNode() : l_info{ 0 }, l_next{nullptr}{}
	
	ListNode* ListNode::InsertNode(ListNode*& p, int i)
	{
		ListNode* q = new ListNode;
		assert(q && "Память не выделилась!!!");
		q->l_info = i;
		if (!p) // если список ещё не заполнен ни одним элементом
			p = q;
		else
		{
			q->l_next = p->l_next;
			p->l_next = q;
		}
		return this;
	}

	int ListNode::DeleteNode(ListNode* p)
	{
		ListNode* q = p->l_next;
		int val = q->l_info;
		p->l_next = q->l_next;
		delete q;
		return val;
	}

	ListNode* ListNode::PrintList(ListNode* p)
	{
		std::cout << "Список:\n";
		do
		{
			std::cout << p->l_info << ' ';
			p = p->l_next;
		} while (p != BeginList);
		std::cout << "\n";
		return this;
	}

	ListNode* ListNode::Rationing(ListNode* p)
	{
		do 
		{
			if (p->l_info > 0)
				p->l_info -= p->l_next->l_info;
			else p->l_info += p->l_next->l_info;
			p = p->l_next;
		} while (p != BeginList);
		return this;
	}

	ListNode* ListNode::Dispose()
	{
		while (BeginList != BeginList->l_next)
			DeleteNode(BeginList);
		delete[] BeginList;
		return this;
	}
}