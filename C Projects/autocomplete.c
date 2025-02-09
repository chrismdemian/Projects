#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void read_in_terms(term **terms, int *pnterms, char *filename) {

// Takes in a pointer to a term, pointer to a number of terms, and a pointer to a txt file

// Allocates momory for every term in file

// Reads in all terms from filename, places them in the block with pointer *terms, sorted in lexicographic order

// Stores a pointer to the block in *terms, stores number of terms in *pnterms

}

int lowest_match(term *terms, int nterms, char *substr) {

// Terms are sorted in lexicographic order

// Returns index in terms of the first term in lexicographic ordering that matches the string substr, O(log(n)) efficiency

}

int highest_match(struct term *terms, int nterms, char *substr) {

// Terms are sorted in lexicographic order

// Returns index in terms of the last term in lexicographic ordering that matches the string substr, O(log(n)) efficiency

}

void autocomplete(term **answer, int *n_answer, term *terms, int nterms, char *substr) {

// Takes in terms sorted in increasing lexicographic order, number of terms nterms, and query string substr

// Places the answer in answer, with *n_answer being the number of answers

// Answers are sorted by weight in non-decreasing order using qsort

}

int main() {

    // Creates basic term structure

    typedef struct term{
        char term[200];
        double weight;
        } term;
        
    
        
    return 0;
}