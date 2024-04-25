{% include 'header.html' %}
<script>
  // 在页面加载前，使用 JavaScript 动态设置标题
  window.onload = function() {
    document.title = "Nmap";
  };

  // 隐藏查询结果的部分
  document.getElementById("queryResults").style.display = "none";

  // 显示查询结果的部分并隐藏其他信息输入框
  function showResults() {
    // 显示查询结果的部分
    document.getElementById("queryResults").style.display = "block";
    // 隐藏其他信息输入框
    document.getElementById("otherInfoInput").style.display = "none";
    // 隐藏网段信息输入框
    document.getElementById("networkInput").style.display = "none";
  }

  // 显示其他人信息的输入框并隐藏查询结果的部分
  function showOtherInfoInput() {
    // 显示其他信息输入框
    document.getElementById("otherInfoInput").style.display = "block";
    // 隐藏查询结果的部分
    document.getElementById("queryResults").style.display = "none";
    // 隐藏网段信息输入框
    document.getElementById("networkInput").style.display = "none";
  }

  // 显示网段信息的输入框并隐藏查询结果的部分和其他信息输入框
  function showNetworkInput() {
    // 显示网段信息输入框
    document.getElementById("networkInput").style.display = "block";
    // 隐藏查询结果的部分
    document.getElementById("queryResults").style.display = "none";
    // 隐藏其他信息输入框
    document.getElementById("otherInfoInput").style.display = "none";
  }

  // 返回到菜单页面
  function goBackToMenu() {
      window.location.href = "/menu";
  }
</script>
<link rel="stylesheet" href="/static/css/bootstrap.min.css"/>
<div class="container mt-5">
    <div class="row">
        <div class="col-md-6 bg-primary-light">
            <h2>查询</h2>
            <form id="userForm" action="{{ url_for('nmapfun') }}" method="POST">
                <input type="hidden" name="action" value="query_myself">
                <button type="submit" class="btn btn-primary" onclick="showResults()">查看你的主机</button>
            </form>
            <form id="otherForm" action="{{ url_for('nmapfun') }}" method="POST">
                <input type="hidden" name="action" value="query_other_user">
                <button type="button" class="btn btn-secondary" onclick="showOtherInfoInput()">查看其他主机</button>
                <div id="otherInfoInput" style="display: none;">
                    <input type="text" name="ip" placeholder="输入 IP 地址，例如192.168.1.1" required pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" class="form-control mb-2">
                    <button type="submit" class="btn btn-primary">提交</button>
                </div>
            </form>
            <form id="networkForm" action="{{ url_for('nmapfun') }}" method="POST">
                <input type="hidden" name="action" value="query_network">
                <button type="button" class="btn btn-info" onclick="showNetworkInput()">查看网段信息</button>
                <div id="networkInput" style="display: none;">
                    <input type="text" name="network" placeholder="输入 IP 网段" required pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}" class="form-control mb-2">
                    <button type="submit" class="btn btn-primary">提交</button>
                </div>
            </form>
            <!-- 返回按钮 -->
            <button type="button" class="btn btn-outline-primary mt-3" onclick="goBackToMenu()">返回</button>
        </div>
        <div class="col-md-6 bg-light">
            <div id="queryResults" style="max-height: 400px; overflow-y: auto;">
                {% if result %}
                    <h2>查询结果:</h2>
                    <ul>
                        {% for host_info in result %}
                            <li>
                                <strong>{{ host_info['host'] }}</strong> <!-- 主机信息作为一级列表项 -->
                                <ul>
                                    {% if host_info['ports'] %}
                                        {% for port_info in host_info['ports'] %}
                                            <li>Port: {{ port_info['port'] }}, Service: {{ port_info['service'] }}</li> <!-- 端口信息作为二级列表项 -->
                                        {% endfor %}
                                    {% endif %}
                                    {% if host_info['os_info'] %}
                                        <li>Operating System: {{ host_info['os_info']['osfamily'] }} {{ host_info['os_info']['osgen'] }}</li> <!-- 操作系统信息作为二级列表项 -->
                                    {% endif %}
                                </ul>
                            </li>
                        {% endfor %}
                    </ul>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% include 'footer.html' %}
