//shader vertex
# version 330 core

layout(location = 0) in vec3 a_position;
layout(location = 1) in float a_index;
layout(location = 2) in vec2 a_textue_offset;

out VS_OUT {
    float v_index;
    vec2 v_textue_offset;
} vs_out;


void main()
{
    gl_Position = vec4(a_position, 1.0f);
    vs_out.v_index = a_index;
    vs_out.v_textue_offset = a_textue_offset;
}




//shader geometry
# version 330 core

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

in VS_OUT {
    float v_index;
    vec2 v_textue_offset;
} gs_in[];

out vec2 uv;

uniform mat4 projection;
uniform mat4 view;
uniform vec3 chunk_position;
uniform float atlas_rows;

mat4 quad = mat4(
    -1.0,  1.0,  1.0, 0.0,
    -1.0, -1.0,  1.0, 0.0,
    1.0,  1.0,  1.0, 0.0, 
    1.0, -1.0,  1.0, 0.0
);
// vec3(-1.0,  1.0,  1.0)
// vec3(-1.0, -1.0,  1.0)
// vec3( 1.0,  1.0,  1.0)
// vec3( 1.0, -1.0,  1.0)

mat3 rot_x = mat3(
    1,  0,  0,
    0,  0, -1,
    0,  1,  0
);
mat3 rot_y = mat3(
    0,  0,  1,
    0,  1,  0,
   -1,  0,  0
);
mat3 rot_z = mat3(
    0, -1,  0,
    1,  0,  0,
    0,  0,  1
);

int index = int(gs_in[0].v_index);



void createVertex(vec3 offset)
{   
    offset *= 0.5;
    vec3 originalPosition = vec3(offset);
    vec4 actualOffset = vec4(originalPosition * rot_z, 0.0);
    switch(index) {
    case 0:
        break;
    case 2:
        actualOffset = vec4(originalPosition * rot_y * rot_x, 0.0);
        break;
    case 4:
        actualOffset =  vec4(originalPosition * rot_x, 0.0);
        break;
    case 1:
        actualOffset =  vec4(originalPosition * rot_x * rot_x * rot_z, 0.0);
        break;
    case 3:
        actualOffset =  vec4(originalPosition * rot_y * rot_y * rot_y * rot_x * rot_x * rot_x, 0.0);
        break;
    case 5:
        actualOffset =  vec4(originalPosition * rot_x * rot_x * rot_x, 0.0);
        break;
    }

    vec4 worldPosition = gl_in[0].gl_Position + actualOffset + vec4(chunk_position, 0.0);
    gl_Position = projection * view * worldPosition;
    EmitVertex();
}

void main()
{
    int mod = int(index - (2 * floor(index/2)));

    uv = vec2(1, 1) / atlas_rows + gs_in[0].v_textue_offset;
    createVertex(vec3(quad[0]));
    uv = vec2(0, 1) / atlas_rows + gs_in[0].v_textue_offset;
    createVertex(vec3(quad[1]));
    uv = vec2(1, 0) / atlas_rows + gs_in[0].v_textue_offset;
    createVertex(vec3(quad[2]));
    uv = vec2(0, 0) / atlas_rows + gs_in[0].v_textue_offset;
    createVertex(vec3(quad[3]));

    EndPrimitive();
}




//shader fragment
# version 330 core

in vec2 uv;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, uv);
    // out_color = vec4(1.0f, 1.0f, 1.0f, 1.0f);
}