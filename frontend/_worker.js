// Cloudflare Pages Worker: 代理 API 请求到 Render 后端

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // 如果是 API 请求，代理到 Render 后端
    if (url.pathname.startsWith('/api/')) {
      const backendUrl = `https://cs-teachable-agent-api.onrender.com${url.pathname}${url.search}`;
      
      // 创建新的请求头
      const headers = new Headers(request.headers);
      headers.set('Host', 'cs-teachable-agent-api.onrender.com');
      
      // 创建代理请求
      const modifiedRequest = new Request(backendUrl, {
        method: request.method,
        headers: headers,
        body: request.body,
      });
      
      try {
        // 发送请求到后端
        const response = await fetch(modifiedRequest);
        
        // 创建新的响应，添加 CORS 头
        const modifiedResponse = new Response(response.body, {
          status: response.status,
          statusText: response.statusText,
          headers: response.headers,
        });
        
        // 添加 CORS 头
        modifiedResponse.headers.set('Access-Control-Allow-Origin', '*');
        modifiedResponse.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, PATCH');
        modifiedResponse.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');
        modifiedResponse.headers.set('Access-Control-Max-Age', '86400');
        
        return modifiedResponse;
      } catch (error) {
        return new Response(
          JSON.stringify({ 
            error: 'Backend connection failed', 
            details: error.message,
            timestamp: new Date().toISOString()
          }),
          { 
            status: 502,
            headers: { 
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': '*'
            }
          }
        );
      }
    }
    
    // 其他请求使用默认的 Pages 处理（SPA fallback）
    return env.ASSETS.fetch(request);
  },
};
