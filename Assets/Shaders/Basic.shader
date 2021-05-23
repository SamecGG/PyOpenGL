//shader vertex
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_offset;
layout(location = 3) in vec2 a_atlas_offset;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;
uniform mat4 move;
uniform float atlas_rows;

out vec3 v_color;
out vec2 v_texture;

void main()
{
    vec3 final_pos = a_position + a_offset;
    gl_Position = projection * view * move * model * vec4(final_pos, 1.0);
    v_texture = (a_texture / atlas_rows) + a_atlas_offset;
}


//shader fragment
# version 330

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, v_texture);
}