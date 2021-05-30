#include "chunks.h"

Vector3<int> chunkSize(16, 256, 16);
Vector3<int> chunkSizeVec(256 * 16, 16, 1);
Vector3<int> *chunkSizePtr = &chunkSize;
Vector3<int> *chunkSizeVecPtr = &chunkSizeVec;

int blockTypes[2][6] = {
    {1, 1, 1, 1, 1, 1},
    {3, 3, 3, 3, 2, 0}};

int normals[6][3] = {
    0, 0, 1,
    0, 0, -1,
    1, 0, 0,
    -1, 0, 0,
    0, -1, 0,
    0, 1, 0};

void setChunkSize(Vector3<int> &newSize)
{
    *chunkSizePtr = newSize;
    chunkSizeVecPtr = new Vector3<int>(newSize.y * newSize.z, newSize.z, 1);
}

std::vector<int> generateChunkData()
{
    int height = 10;
    std::vector<int> chunkData;
    chunkData.reserve(chunkSize.x * chunkSize.y * chunkSize.z);

    for (int x = 0; x < chunkSize.x; x++)
    {
        for (int y = 0; y < chunkSize.y; y++)
        {
            for (int z = 0; z < chunkSize.z; z++)
            {
                if (y <= height)
                    chunkData.emplace_back(1);
                else
                    chunkData.emplace_back(0);
            }
        }
    }

    return chunkData;
}

std::vector<int *> generateMeshData(int (&chunkData)[])
{
    // 4 vertices per each face
    // 3 * 2 triangle indices per each face
    std::vector<int *> vertices;

    for (int x = 0; x < chunkSize.x; x++)
    {
        for (int y = 0; y < chunkSize.y; y++)
        {
            for (int z = 0; z < chunkSize.z; z++)
            {
                // block variables
                const Vector3<int> blockPosition(x, y, z);
                const int &index = blockPosition | chunkSizeVec;
                int blockType = chunkData[index];
                int(&blockTypeFaces)[6] = blockTypes[blockType];

                if (blockType == 0)
                    continue;

                for (int faceIndex = 0; faceIndex < 6; faceIndex++)
                {
                    Vector3<int> &faceNormal = *new Vector3<int>(normals[faceIndex]);
                    Vector3<int> &checkPosition = blockPosition + faceNormal;

                    if (0 <= checkPosition.x < chunkSize.x && 0 <= checkPosition.y < chunkSize.y && 0 <= checkPosition.z < chunkSize.z)
                    {
                        const int &checkIndex = checkPosition | chunkSizeVec;
                        int *checkBlockType = &chunkData[checkIndex];

                        if (!checkBlockType)
                            vertices.push_back({GenerateFace(blockPosition, faceIndex, blockTypeFaces[faceIndex])});
                    }
                    else
                        vertices.push_back({GenerateFace(blockPosition, faceIndex, blockTypeFaces[faceIndex])});
                }
            }
        }
    }
    return vertices;
}

int *GenerateFace(Vector3<int> blockPosition, int faceIndex, int textureIndex)
{
    int *data[] = {&blockPosition.x, &blockPosition.y, &blockPosition.z, &faceIndex, &textureIndex};

    return *data;
}

std::vector<int *> loadChunk(Vector3<int> &position)
{
    char path_buffer[50];
    sprintf(path_buffer, "chunks/%d_%d.txt", position.x, position.z);

    std::ifstream file(path_buffer);
    std::vector<int> chunkData;

    if (!file.is_open())
    {
        // no file
        std::cout << "There's no file" << std::endl;

        chunkData = generateChunkData();
    }
    else
    {
        // read file
        std::cout << "Read file" << std::endl;
        std::string fileText;
        chunkData.reserve(chunkSize.x * chunkSize.y * chunkSize.z);
        const int dataSize = chunkSize.x * chunkSize.z;
        //std::string data[data_size];

        while (std::getline(file, fileText, ' '))
        {
            // Output the text from the file
            std::cout << fileText << std::endl;
            chunkData.emplace_back(fileText);
        }

        file.close();
    }

    std::vector<int *> meshData = generateMeshData(chunkData);

    return meshData;
}

int saveChunk(Vector3<int> &position, std::vector<int> &chunkData)
{
    std::ofstream file;

    char pathBuffer[50];
    sprintf(pathBuffer, "chunks/%d_%d.txt", position.x, position.z);

    std::ofstream file(pathBuffer);

    for (int blockData : chunkData)
    {
        file << blockData << ' ';
    }

    file.close();
    return 0;
}
