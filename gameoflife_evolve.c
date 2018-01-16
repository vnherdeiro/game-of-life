#include <stdlib.h>
#include <stdio.h>

void evolve( int * conf, const int size){
	//allocating array storing number of neighbours alive
	int ** neighbours = (int **) malloc(size * sizeof(int *));
	for( int i = 0; i < size; ++i)
		neighbours[i] = (int *) malloc( size * sizeof(int));

	//filling neighbours information
	for( int i = 0; i < size; ++i){
		const int prev_i = ((i-1) + size ) % size;
		const int next_i = (i+1) % size;
		for( int j = 0; j < size; ++j){
			const int prev_j = ((j-1) + size ) % size;
			const int next_j = (j+1) % size;
			neighbours[i][j] = conf[prev_i*size + prev_j] + conf[prev_i*size + j] + conf[prev_i*size + next_j] + conf[i*size + prev_j] + conf[i*size + next_j] + conf[next_i*size + prev_j] + conf[next_i*size + j] + conf[next_i*size + next_j];
			}
		}

	//updating configuration inplace
	for( int i = 0; i < size; ++i){
		for( int j = 0; j < size; ++j){
			conf[i*size + j] = (int) (neighbours[i][j] == 3) || ((conf[i*size + j] == 1) && (neighbours[i][j] == 2));
			}
		}

	for( int i = 0; i < size; ++i)
		free( neighbours[i]);
	free( neighbours);
}
