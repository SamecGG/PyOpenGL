//shader vertex
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_offset;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;
uniform mat4 move;

out vec2 v_texture;

void main()
{
    vec3 final_pos = a_position + a_offset;
    gl_Position = projection * move * view * model * vec4(final_pos, 1.0f);
    v_texture = a_texture;
}


//shader fragment
# version 330

in vec2 v_texture;

out vec4 out_color;

uniform sampler2DArray s_texture;

void main()
{
    out_color = texture(s_texture, vec3(v_texture, 1));
}