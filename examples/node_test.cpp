#include "drmemory_annotations.h"

class Node{
    public:
    Node* next;
    int val;
};

int main(){
    Node* a = new Node();
    Node* b = new Node();
    Node* c = new Node();
    Node* d = new Node();
    Node* e = new Node();
    Node* f = new Node();

    a->val = 1;
    b->val = 2;
    c->val = 3;
    d->val = 4;
    e->val = 5;
    f->val = 6;

    a->next = b;
    b->next = c;
    c->next = d;
    d->next = e;
    e->next = f;
    f->next = nullptr;

    DRMEMORY_ANNOTATE_DUMP_MEMORY_LAYOUT();
    
    delete a;
    delete b;
    delete c;
    delete d;
    delete e;
    delete f;
}