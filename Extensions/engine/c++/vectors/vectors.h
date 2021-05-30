#pragma once

template <typename T>
struct Vector3
{
    T x, y, z;

    Vector3();
    Vector3(const T x = 0.0f, const T y = 0.0f, const T z = 0.0f);
    Vector3(const T position[3]);

    // Adding
    Vector3 operator+(const Vector3 &other) const;

    // Subtracting
    Vector3 operator-(const Vector3 &other) const;

    // Multiplying
    Vector3 operator*(const Vector3 &other) const;

    // Dividing
    Vector3 operator/(const Vector3 &other) const;y / other.y, z / other.z);

    // DOT product
    T operator|(const Vector3 &other) const;
};
