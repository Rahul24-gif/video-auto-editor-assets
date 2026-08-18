// RGB Chromatic Aberration Glitch GLSL Transition Shader

#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D from;
uniform sampler2D to;
uniform float progress;
uniform vec2 resolution;

float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

void main() {
    vec2 uv = gl_FragCoord.xy / resolution.xy;
    
    // Intensity peaks at progress = 0.5
    float glitchIntensity = sin(progress * 3.14159265);
    
    // Block displacement
    float block = floor(uv.y * 24.0);
    float noise = random(vec2(block, floor(progress * 12.0))) * 2.0 - 1.0;
    
    vec2 offset = vec2(noise * 0.06 * glitchIntensity, 0.0);
    
    // Split RGB
    vec2 rOffset = offset * 1.5;
    vec2 bOffset = -offset * 1.2;
    
    vec4 fromColor = vec4(
        texture2D(from, uv + rOffset).r,
        texture2D(from, uv + offset).g,
        texture2D(from, uv + bOffset).b,
        1.0
    );
    
    vec4 toColor = vec4(
        texture2D(to, uv + rOffset).r,
        texture2D(to, uv + offset).g,
        texture2D(to, uv + bOffset).b,
        1.0
    );
    
    gl_FragColor = mix(fromColor, toColor, progress);
}
