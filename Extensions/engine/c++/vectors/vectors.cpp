#include "vectors.h"

template <typename T>
Vector3<T>::Vector3()
{
    this->x = (T)0;
    this->y = (T)0;
    this->z = (T)0;
}

template <typename T>
Vector3<T>::Vector3(const T x = 0.0f, const T y = 0.0f, const T z = 0.0f)
{
    this->x = (T)x;
    this->y = (T)y;
    this->z = (T)z;
}

template <typename T>
Vector3<T>::Vector3(const T position[3])
{
    this->x = position[0];
    this->y = position[1];
    this->z = position[2];
}

// Adding
template <typename T>
Vector3<T> Vector3<T>::operator+(const Vector3<T> &other) const
{
    return Vector3(x + other.x, y + other.y, z + other.z);
}

// Subtracting
template <typename T>
Vector3<T> Vector3<T>::operator-(const Vector3<T> &other) const
{
    return Vector3(x - other.x, y - other.y, z - other.z);
}

// Multiplying
template <typename T>
Vector3<T> Vector3<T>::operator*(const Vector3<T> &other) const
{
    return Vector3(x * other.x, y * other.y, z * other.z);
}

// Dividing
template <typename T>
Vector3<T> Vector3<T>::operator/(const Vector3<T> &other) const
{
    return Vector3(x / other.x, y / other.y, z / other.z);
}

// DOT product
template <typename T>
T Vector3<T>::operator|(const Vector3<T> &other) const
{
    return T(x * other.x + y * other.y + z * other.z);
}
