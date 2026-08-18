// Luma Matte Wipe GLSL Transition Shader

#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D from;
uniform sampler2D to;
uniform sampler2D lumaMatte;
uniform float progress;
uniform vec2 resolution;

void main() {
    vec2 uv = gl_FragCoord.xy / resolution.xy;
    
    vec4 fromCol = texture2D(from, uv);
    vec4 toCol = texture2D(to, uv);
    
    // Read luma mask
    float mask = texture2D(lumaMatte, uv).r;
    
    // Smooth threshold edge
    float softness = 0.08;
    float alpha = smoothstep(progress - softness, progress + softness, mask);
    
    gl_FragColor = mix(toCol, fromCol, alpha);
}
