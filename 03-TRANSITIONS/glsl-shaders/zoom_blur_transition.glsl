// Zoom Blur GLSL Transition Shader for GPU / WebGL / Remotion Compositors
// Uniforms: progress (0.0 to 1.0), resolution (vec2), strength (float)

#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D from;
uniform sampler2D to;
uniform float progress;
uniform vec2 resolution;

const float STRENGTH = 0.35;
const int SAMPLES = 16;

vec4 getFromColor(vec2 uv) {
    return texture2D(from, uv);
}

vec4 getToColor(vec2 uv) {
    return texture2D(to, uv);
}

void main() {
    vec2 uv = gl_FragCoord.xy / resolution.xy;
    vec2 center = vec2(0.5, 0.5);
    vec2 toCenter = center - uv;
    
    vec4 c1 = vec4(0.0);
    vec4 c2 = vec4(0.0);
    
    float total = 0.0;
    float offset = progress * STRENGTH;
    
    for (int i = 0; i < SAMPLES; i++) {
        float percent = (float(i) + 0.5) / float(SAMPLES);
        float weight = 4.0 * (percent - percent * percent);
        c1 += getFromColor(uv + toCenter * percent * offset) * weight;
        c2 += getToColor(uv - toCenter * (1.0 - percent) * (1.0 - progress) * STRENGTH) * weight;
        total += weight;
    }
    
    c1 /= total;
    c2 /= total;
    
    gl_FragColor = mix(c1, c2, smoothstep(0.3, 0.7, progress));
}
