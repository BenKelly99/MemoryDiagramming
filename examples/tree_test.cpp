#include "drmemory_annotations.h"

class Node{
    public:
    Node* left;
    Node* right;
    int val;
};

int main(){
    Node* head = new Node();
    head->left = new Node();
    head->left->left = new Node();
    head->left->left->right = new Node();
    head->left->right = new Node();
    head->right = new Node();
    head->right->left = new Node();
    head->right->left->left = new Node();
    head->right->right = new Node();

    DRMEMORY_ANNOTATE_DUMP_MEMORY_LAYOUT();
}
