// Cloudflare Pages Function: 代理所有 /api/* 请求到 Railway 后端

export const onRequest: PagesFunction = async (context) => {
  const { request, params } = context;
  const path = params.path || [];
  const pathString = Array.isArray(path) ? path.join('/') : path;
  
  // Railway 后端地址
  const backendUrl = `https://cs-teachable-agent-production.up.railway.app/api/${pathString}`;
  
  // 复制原始请求的 header
  const headers = new Headers(request.headers);
  headers.delete('host'); // 移除原始 host，让 Cloudflare 自动设置
  
  // 创建新的请求
  const modifiedRequest = new Request(backendUrl, {
    method: request.method,
    headers: headers,
    body: request.body,
  });
  
  try {
    // 转发请求到后端
    const response = await fetch(modifiedRequest);
    
    // 创建新的响应，添加 CORS 头
    const modifiedResponse = new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: response.headers,
    });
    
    // 添加 CORS 头
    modifiedResponse.headers.set('Access-Control-Allow-Origin', '*');
    modifiedResponse.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    modifiedResponse.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    return modifiedResponse;
  } catch (error) {
    return new Response(
      JSON.stringify({ error: 'Backend connection failed', details: String(error) }),
      { 
        status: 502,
        headers: { 
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }
    );
  }
};
