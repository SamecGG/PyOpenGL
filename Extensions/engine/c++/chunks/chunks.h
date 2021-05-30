#pragma once
#include "../vectors/vectors.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

Vector3<int> chunkSize;

void setChunkSize(Vector3<int> &newSize);

std::vector<int*> loadChunk(Vector3<int> &position);
int saveChunk(Vector3<int> &position, std::vector<int> &chunkData);

std::vector<int> generateChunkData();
std::vector<int*> generateMeshData(std::vector<int> &chunkdata);