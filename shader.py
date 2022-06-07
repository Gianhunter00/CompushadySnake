shader_clean_screen = """
RWTexture2D<float4> target : register(u0);

[numthreads(4, 1, 1)]
void main(int3 tid : SV_DispatchThreadID)
{
    target[tid.xy] = float4(0, 0, 0, 0);
}
"""
shader_code = """
RWTexture2D<float4> target : register(u0);
Buffer<int4> quads : register(t0);

[numthreads(8, 8, 1)]
void main(uint3 tid : SV_DispatchThreadID)
{
int4 quad = quads[tid.z];
   
    if (tid.x > quad.x + quad.z)
        return;
    if (tid.x < quad.x)
        return;
    if (tid.y < quad.y)
        return;
    if (tid.y > quad.y + quad.w)
        return;
    if(quad.z == 19)
        target[tid.xy] = float4(1, 0, 0, 1);
    else
        target[tid.xy] = float4(0, 1, 0, 1);
        
}
"""