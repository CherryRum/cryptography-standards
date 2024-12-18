# cryptography-standards
该仓库收录了多种密码学标准，主要包括中国的商用密码（SM系列）以及其他常见的密码学标准，如中国密码国家标准、行业标准等。本项目目的是为了方便开发者了解并实现这些标准，同时为密码学研究和开发提供一些参考。
### 包含的标准：
1. **国密标准（SM系列）**：
    - `SM2`: 公钥密码算法
    - `SM3`: 哈希算法
    - `SM4`: 对称加密算法
    - `SM9`: 标识密码算法
2. **中国密码国家标准和行业标准** `如下表`
<body>
<!-- <style>
  /* 表格整体样式 */
  table {
    width: 100%;
    color:royalblue;
    border-collapse: collapse;
    margin: 10px 2px; 
    background-color: #69293a;
  }
  /* 表头单元格样式 */
  th {
    font-weight: bold;
    border: 1px solid #d2b0b0;
    text-align: center;
    background-color: #bb6060; /* 添加背景颜色，使表头更突出 */
    padding: 10px; /* 增加内边距，使内容更宽松 */
  }
  /* 普通单元格样式 */
  td {
    text-align: justify;
    padding: 5px;
  }
  tbody tr:hover {
    background-color: rgba(117,239,140,0.71);
    color: rgb(11,56,236);
  }
</style> -->
<table class="xl65">
 <tbody>
  <tr > 
    <th colspan="4" >中国密码国家标准、行业标准一览表 ——更新时间：2024年12月18日</th>
  </tr> 
        <tr>
            <th colspan="2" class="xl65">密码国家标准</th>
            <th colspan="2" class="xl65">密码行业标准</th>
        </tr>
  <tr > 
   <th class="xl65">标准编号</th> 
   <th class="xl65">标准名称</th> 
   <th class="xl65">标准编号</th> 
   <th class="xl65">标准名称</th> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 33133.1-2016</td> 
   <td class="xl66">信息安全技术 祖冲之序列密码算法 第1部分：算法描述</td> 
   <td class="xl66">GM/T 0001.1-2012</td> 
   <td class="xl66">祖冲之序列密码算法 第1部分：算法描述</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 33133.2-2021</td> 
   <td class="xl66">信息安全技术 祖冲之序列密码算法 第2部分：保密性算法</td> 
   <td class="xl66">GM/T 0001.2-2012</td> 
   <td class="xl66">祖冲之序列密码算法 第2部分：基于祖冲之算法的机密性算法</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 33133.3-2021</td> 
   <td class="xl66">信息安全技术 祖冲之序列密码算法 第3部分：完整性算法</td> 
   <td class="xl66">GM/T 0001.3-2012</td> 
   <td class="xl66">祖冲之序列密码算法 第3部分：基于祖冲之算法的完整性算法</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 32907-2016</td> 
   <td class="xl66">信息安全技术 SM4分组密码算法</td> 
   <td class="xl66">GM/T 0002-2012</td> 
   <td class="xl66">SM4分组密码算法</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 32918.1-2016</td> 
   <td class="xl66">信息安全技术 SM2圆曲线公钥密码算法 第1部分：总则</td> 
   <td class="xl66">GM/T 0003.1-2012</td> 
   <td class="xl66">SM2圆曲线公钥密码算法 第 1部分：总则</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 32918.2-2016</td> 
   <td class="xl66">信息安全技术 SM2 圆曲线公钥密码算法 第2部分：数字签名算法</td> 
   <td class="xl66">GM/T 0003.2-2012</td> 
   <td class="xl66">SM2 圆曲线公钥密码算法 第2部分：数字签名算法</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 32918.3-2016</td> 
   <td class="xl66">信息安全技术 SM2 圆曲线公钥密码算法 第3 部分：密钥交换协议</td> 
   <td class="xl66">GM/T 0003.3-2012</td> 
   <td class="xl66">SM2 圆曲线公钥密码算法 第3部分：密钥交换协议</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 32918.4-2016</td> 
   <td class="xl66">信息安全技术 SM2 圆曲线公钥密码算法 第4部分：公钥加密算法</td> 
   <td class="xl66">GM/T 0003.4-2012</td> 
   <td class="xl66">SM2 圆曲线公钥密码算法 第4部分：公钥加密算法</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 32918.5-2017</td> 
   <td class="xl66">信息安全技术 SM2 圆曲线公钥密码算法 第5部分：参数定义</td> 
   <td class="xl66">GM/T 0003.5-2012</td> 
   <td class="xl66">SM2 圆曲线公钥密码算法 第5部分：参数定义</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 32905-2016</td> 
   <td class="xl66">信息安全技术 SM3 密码杂凑算法</td> 
   <td class="xl66">GM/T 0004-2012</td> 
   <td class="xl66">SM3 密码杂凑算法</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 32915-2016</td> 
   <td class="xl66">信息安全技术 二元序列随机性检测方法</td> 
   <td class="xl66">GM/T 0005-2012</td> 
   <td class="xl66">随机性检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 33560-2017</td> 
   <td class="xl66">信息安全技术 密码应用标识规范</td> 
   <td class="xl66">GM/T 0006-2023</td> 
   <td class="xl66">密码应用标识规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0008-2012</td> 
   <td class="xl66">安全芯片密码检测准则</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 35276-2017</td> 
   <td class="xl66">信息安全技术 SM2密码算法使用规范</td> 
   <td class="xl66">GM/T 0009-2023</td> 
   <td class="xl66">SM2密码算法使用规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 35275-2017</td> 
   <td class="xl66">信息安全技术 SM2密码算法加密签名消息语法规范</td> 
   <td class="xl66">GM/T 0010-2023</td> 
   <td class="xl66">SM2 密码算法加密签名消息语法规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 29829-2022</td> 
   <td class="xl66">信息安全技术 可信计算密码支撑平台功能与接口规范</td> 
   <td class="xl66">GM/T 0011-2023</td> 
   <td class="xl66">可信计算 可信密码支撑平台功能与接口规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0012-2020</td> 
   <td class="xl66">可信计算 可信密码模块接口规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0013-2021</td> 
   <td class="xl66">可信计算 可信密码模块接口符合性测试规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0014-2023</td> 
   <td class="xl66">数字证书认证系统密码协议规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 20518-2018</td> 
   <td class="xl66">信息安全技术 公钥基础设施 数字证书格式</td> 
   <td class="xl66">GM/T 0015-2023</td> 
   <td class="xl66">基于SM2密码算法的数字证书格式规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 35291-2017</td> 
   <td class="xl66">信息安全技术 智能密码钥匙应用接口规范</td> 
   <td class="xl66">GM/T 0016-2023</td> 
   <td class="xl66">智能密码钥匙密码应用接口规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0017-2023</td> 
   <td class="xl66">智能密码钥匙密码应用接口数据格式规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 36322-2018</td> 
   <td class="xl66">信息安全技术 密码设备应用接口规范</td> 
   <td class="xl66">GM/T 0018-2023</td> 
   <td class="xl66">密码设备应用接口规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0019-2023</td> 
   <td class="xl66">通用密码服务接口规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0020-2023</td> 
   <td class="xl66">证书应用综合服务接口规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 38556-2020</td> 
   <td class="xl66">信息安全技术 动态口令密码应用技术规范</td> 
   <td class="xl66">GM/T 0021-2023</td> 
   <td class="xl66">动态口令密码应用技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 36968-2018</td> 
   <td class="xl66">信息安全技术 IPSec VPN 技术规范</td> 
   <td class="xl66">GM/T 0022-2023</td> 
   <td class="xl66">IPSecVPN 技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0023-2023</td> 
   <td class="xl66">IPSec VPN 网关产品规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0024-2023</td> 
   <td class="xl66">SSL VPN 技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0025-2023</td> 
   <td class="xl66">SSL VPN 网关产品规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0026-2023</td> 
   <td class="xl66">安全认证网关产品规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0027-2014</td> 
   <td class="xl66">智能密码钥匙技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 37092-2018</td> 
   <td class="xl66">信息安全技术 密码模块安全要求</td> 
   <td class="xl66">GM/T 0028-2014</td> 
   <td class="xl66">密码模块安全技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 38629-2020</td> 
   <td class="xl66">信息安全技术 签名验签服务器技术规范</td> 
   <td class="xl66">GM/T 0029-2014</td> 
   <td class="xl66">签名验签服务器技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0030-2014</td> 
   <td class="xl66">服务器密码机技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 38540-2020</td> 
   <td class="xl66">信息安全技术 安全电子签章密码技术规范</td> 
   <td class="xl66">GM/T 0031-2014</td> 
   <td class="xl66">安全电子签章密码技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0032-2014</td> 
   <td class="xl66">基于角色的授权与访问控制技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0033-2023</td> 
   <td class="xl66">时间戳接口规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 25056-2018</td> 
   <td class="xl66">信息安全技术 证书认证系统密码及其相关安全技术规范</td> 
   <td class="xl66">GM/T 0034-2014</td> 
   <td class="xl66">基于 SM2 密码算法的证书认证系统密码及其相关安全技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 37033.1-2018</td> 
   <td class="xl66">信息安全技术 射频识别系统密码应用技术要求 第1部分：密码安全保护框架及安全级别</td> 
   <td class="xl66">GM/T 0035.1-2014</td> 
   <td class="xl66">射频识别系统密码应用技术要求 第1部分：密码安全保护框架及安全级别</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 37033.2-2018</td> 
   <td class="xl66">信息安全技术 射频识别系统密码应用技术要求 第2部分：电子标签与读写器及其通信密码应用技术要求</td> 
   <td class="xl66">GM/T 0035.2-2014</td> 
   <td class="xl66">射频识别系统密码应用技术要求 第2部分：电子标签芯片密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 37033.3-2018</td> 
   <td class="xl66">信息安全技术 射频识别系统密码应用技术要求 第3部分：密钥管理技术要求</td> 
   <td class="xl66">GM/T 0035.3-2014</td> 
   <td class="xl66">射频识别系统密码应用技术要求 第３部分：读写器密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0035.4-2014</td> 
   <td class="xl66">射频识别系统密码应用技术要求 第４部分：电子标签与读写器通信密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0035.5-2014</td> 
   <td class="xl66">射频识别系统密码应用技术要求 第５部分：密钥管理技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0036-2014</td> 
   <td class="xl66">采用非接触卡的门禁系统密码应用技术指南</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0037-2014</td> 
   <td class="xl66">证书认证系统检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0038-2014</td> 
   <td class="xl66">证书认证密钥管理系统检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 38625-2020</td> 
   <td class="xl66">信息安全技术 密码模块安全检测要求</td> 
   <td class="xl66">GM/T 0039-2015</td> 
   <td class="xl66">密码模块安全检测要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0040-2015</td> 
   <td class="xl66">射频识别标签模块密码检测准则</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0041-2015</td> 
   <td class="xl66">智能IC卡密码检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0042-2015</td> 
   <td class="xl66">三元对等密码安全协议测试规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0043-2015</td> 
   <td class="xl66">数字证书互操作检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 38635.1-2020</td> 
   <td class="xl66">信息安全技术 SM9标识密码算法第1部分：总则</td> 
   <td class="xl66">GM/T 0044.1-2016</td> 
   <td class="xl66">SM9 标识密码算法 第1部分：总则</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 38635.2-2020</td> 
   <td class="xl66">信息安全技术 SM9标识密码算法第2部分：算法</td> 
   <td class="xl66">GM/T 0044.2-2016</td> 
   <td class="xl66">SM9 标识密码算法 第2部分：数字签名算法</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0044.3-2016</td> 
   <td class="xl66">SM9 标识密码算法 第3部分：密钥交换协议</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0044.4-2016</td> 
   <td class="xl66">SM9 标识密码算法 第4部分：密钥封装机制和公钥加密算法</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0044.5-2016</td> 
   <td class="xl66">SM9 标识密码算法 第5部分：参数定义</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0045-2016</td> 
   <td class="xl66">金融数据密码机技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0046-2016</td> 
   <td class="xl66">金融数据密码机检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0047-2016</td> 
   <td class="xl66">安全电子签章密码检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0048-2016</td> 
   <td class="xl66">智能密码钥匙密码检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0049-2016</td> 
   <td class="xl66">密码键盘密码检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0050-2016</td> 
   <td class="xl66">密码设备管理 设备管理技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0051-2016</td> 
   <td class="xl66">密码设备管理 对称密钥管理技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0052-2016</td> 
   <td class="xl66">密码设备管理 VPN设备监察管理规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0053-2016</td> 
   <td class="xl66">密码设备管理 远程监控与合规性检验接口数据规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 39786-2021</td> 
   <td class="xl66">信息安全技术 信息系统密码应用基本要求</td> 
   <td class="xl66">GM/T 0054-2018</td> 
   <td class="xl66">信息系统密码应用基本要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0055-2018</td> 
   <td class="xl66">电子文件密码应用技术规范（报批稿）</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0056-2018</td> 
   <td class="xl66">多应用载体密码应用接口规范（报批稿）</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0057-2018</td> 
   <td class="xl66">基于IBC技术的身份鉴别规范（报批稿）</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0058-2018</td> 
   <td class="xl66">可信计算TCM服务模块接口规范（报批稿）</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0059-2018</td> 
   <td class="xl66">服务器密码机检测规范（报批稿）</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0060-2018</td> 
   <td class="xl66">签名验签服务器检测规范（报批稿）</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0061-2018</td> 
   <td class="xl66">动态口令密码应用检测规范（报批稿）</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0062-2018</td> 
   <td class="xl66">密码产品随机数检测要求（报批稿）</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0063-2018</td> 
   <td class="xl66">智能密码钥匙密码应用接口检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0064-2018</td> 
   <td class="xl66">限域通信（RCC）密码检测要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0065-2019</td> 
   <td class="xl66">商用密码产品生产和保障能力建设规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0066-2019</td> 
   <td class="xl66">商用密码产品生产和保障能力建设实施指南</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0067-2019</td> 
   <td class="xl66">基于数字证书的身份鉴别接口规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0068-2019</td> 
   <td class="xl66">开放的第三方资源授权协议框架</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0069-2019</td> 
   <td class="xl66">开放的身份鉴别框架</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0070-2019</td> 
   <td class="xl66">电子保单密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 38541-2020</td> 
   <td class="xl66">信息安全技术 电子文件密码应用指南</td> 
   <td class="xl66">GM/T 0071-2019</td> 
   <td class="xl66">电子文件密码应用指南</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0072-2019</td> 
   <td class="xl66">远程移动支付密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0073-2019</td> 
   <td class="xl66">手机银行信息系统密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0074-2019</td> 
   <td class="xl66">网上银行密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0075-2019</td> 
   <td class="xl66">银行信贷信息系统密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0076-2019</td> 
   <td class="xl66">银行卡信息系统密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0077-2019</td> 
   <td class="xl66">银行核心信息系统密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0078-2020</td> 
   <td class="xl66">密码随机数生成模块设计指南</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0079-2020</td> 
   <td class="xl66">可信计算平台直接匿名证明规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 41389-2022</td> 
   <td class="xl66">信息安全技术 SM9密码算法使用规范</td> 
   <td class="xl66">GM/T 0080-2020</td> 
   <td class="xl66">SM9密码算法使用规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0081-2020</td> 
   <td class="xl66">SM9密码算法加密签名消息语法规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0082-2020</td> 
   <td class="xl66">可信密码模块保护轮廓</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0083-2020</td> 
   <td class="xl66">密码模块非入侵式攻击缓解技术指南</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0084-2020</td> 
   <td class="xl66">密码模块物理攻击缓解技术指南</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0085-2020</td> 
   <td class="xl66">基于SM9标识密码算法的技术体系框架</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0086-2020</td> 
   <td class="xl66">基于SM9标识密码算法的密钥管理系统技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0087-2020</td> 
   <td class="xl66">浏览器密码应用接口规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0088-2020</td> 
   <td class="xl66">云服务器密码机管理接口规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0089-2020</td> 
   <td class="xl66">简单证书注册协议规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0090-2020</td> 
   <td class="xl66">标识密码应用标识格式规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0091-2020</td> 
   <td class="xl66">基于口令的密钥派生规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0092-2020</td> 
   <td class="xl66">基于SM2算法的证书申请语法规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0093-2020</td> 
   <td class="xl66">证书与密钥交换格式规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0094-2020</td> 
   <td class="xl66">公钥密码应用技术体系框架规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0095-2020</td> 
   <td class="xl66">电子招投标密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0096-2020</td> 
   <td class="xl66">射频识别防伪系统密码应用指南</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0097-2020</td> 
   <td class="xl66">射频识别电子标签统一名称解析服务安全技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0098-2020</td> 
   <td class="xl66">基于IP网络的加密语音通信密码技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0099-2020</td> 
   <td class="xl66">开放式版式文档密码应用技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0100-2020</td> 
   <td class="xl66">人工确权型数字签名密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0101-2020</td> 
   <td class="xl66">近场通信密码安全协议检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0102-2020</td> 
   <td class="xl66">密码设备应用接口符合性检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0103-2021</td> 
   <td class="xl66">随机数发生器总体框架</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0104-2021</td> 
   <td class="xl66">云服务器密码机技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0105-2021</td> 
   <td class="xl66">软件随机数发生器设计指南</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0106-2021</td> 
   <td class="xl66">银行卡终端产品密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0107-2021</td> 
   <td class="xl66">智能IC卡密钥管理系统基本技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0108-2021</td> 
   <td class="xl66">诱骗态84量子密钥分配产品技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0109-2021</td> 
   <td class="xl66">基于云计算的电子签名服务技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0110-2021</td> 
   <td class="xl66">密钥管理互操作协议规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0111-2021</td> 
   <td class="xl66">区块链密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0112-2021</td> 
   <td class="xl66">PDF 格式文档的密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0113-2021</td> 
   <td class="xl66">在线快捷身份鉴别协议</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0114-2021</td> 
   <td class="xl66">诱骗态BB84量子密钥分配产品检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 43206-2023</td> 
   <td class="xl66">信息安全技术 信息系统密码应用测评要求</td> 
   <td class="xl66">GM/T 0115-2021</td> 
   <td class="xl66">信息系统密码应用测评要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0116-2021</td> 
   <td class="xl66">信息系统密码应用测评过程指南</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0117-2022</td> 
   <td class="xl66">网络身份服务密码应用技术要求</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0118-2022</td> 
   <td class="xl66">浏览器数字证书应用接口规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0119-2022</td> 
   <td class="xl66">PLC控制系统及PLC控制器密码应用技术规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0120-2022</td> 
   <td class="xl66">基于云计算的电子签名服务技术实施指南</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0121-2022</td> 
   <td class="xl66">密码卡检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0122-2022</td> 
   <td class="xl66">区块链密码检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0123-2022</td> 
   <td class="xl66">时间戳服务器密码检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0124-2022</td> 
   <td class="xl66">安全隔离与信息交换产品密码检测规范</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0125.1-2022</td> 
   <td class="xl66">JSON Web 密码应用语法规范 第1部分：算法标识</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0125.2-2022</td> 
   <td class="xl66">JSON Web 密码应用语法规范 第2部分：数字签名</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0125.3-2022</td> 
   <td class="xl66">JSON Web 密码应用语法规范 第3部分：数据加密</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/T 0125.4-2022</td> 
   <td class="xl66">JSON Web 密码应用语法规范 第4部分：密钥</td> 
  </tr> 
  <tr > 
   <td rowspan="8" class="xl66">　</td> 
   <td rowspan="8" class="xl66">　</td> 
   <td class="xl73">GM/T 0126-2023</td> 
   <td class="xl66">HTML密码应用置标语法</td> 
  </tr> 
  <tr > 
   <td class="xl73">GM/T 0127-2023</td> 
   <td class="xl66">移动终端密码模块应用接口规范</td> 
  </tr> 
  <tr > 
   <td class="xl73">GM/T 0128-2023</td> 
   <td class="xl66">数据报传输层密码协议规范</td> 
  </tr> 
  <tr > 
   <td class="xl73">GM/T 0129-2023</td> 
   <td class="xl66">SSH密码协议规范</td> 
  </tr> 
  <tr > 
   <td class="xl73">GM/T 0130-2023</td> 
   <td class="xl66">基于SM2算法的无证书及隐式证书公钥机制</td> 
  </tr> 
  <tr > 
   <td class="xl73">GM/T 0131-2023</td> 
   <td class="xl66">电子签章应用接口规范</td> 
  </tr> 
  <tr > 
   <td class="xl73">GM/T 0132-2023</td> 
   <td class="xl66">信息系统密码应用实施指南</td> 
  </tr> 
  <tr > 
   <td class="xl66">GM/Y 5001-2023</td> 
   <td class="xl66">密码标准使用指南</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/Y 5002-2018</td> 
   <td class="xl66">云计算身份鉴别服务密码标准体系</td> 
  </tr> 
  <tr > 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
   <td class="xl66">GM/Z 4001-2013</td> 
   <td class="xl66">密码术语</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 18238.1-2000</td> 
   <td class="xl66">信息技术 安全技术 散列函数 第1部分：概述</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 18238.2-2002</td> 
   <td class="xl66">信息技术 安全技术 散列函数 第2部分：采用n位块密码的散列函数</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 18238.3-2002</td> 
   <td class="xl66">信息技术 安全技术 散列函数 第3部分：专用散列函数</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 16264.8-2005</td> 
   <td class="xl66">信息技术 开放系统互连 目录 第8部分：公钥和属性证书框架</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 19771-2005</td> 
   <td class="xl66">信息技术 安全技术 公钥基础设施 PKI组件最小互操作规范</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 19713-2005</td> 
   <td class="xl66">信息技术 安全技术 公钥基础设施 在线证书状态协议</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 19714-2005</td> 
   <td class="xl66">信息技术 安全技术 公钥基础设施 证书管理协议</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 17902.1-2023</td> 
   <td class="xl66">信息技术 安全技术 带附录的数字签名 第1部分：概述</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 17902.2-2005</td> 
   <td class="xl66">信息技术 安全技术 带附录的数字签名 第2部分：基于身份的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 17902.3-2005</td> 
   <td class="xl66">信息技术 安全技术 带附录的数字签名 第3部分：基于证书的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 20520-2006</td> 
   <td class="xl66">信息安全技术 公钥基础设施 时间戳规范</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 21054-2023</td> 
   <td class="xl66">信息安全技术 公钥基础设施 PKI系统安全测评方法</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 21053-2023</td> 
   <td class="xl66">信息安全技术 公钥基础设施 PKI系统安全技术要求</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 17903.1-2008</td> 
   <td class="xl66">信息技术 安全技术 抗抵赖 第1部分: 概述</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 17903.2-2021</td> 
   <td class="xl66">信息技术 安全技术 抗抵赖 第2部分: 采用对称技术的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 17903.3-2008</td> 
   <td class="xl66">信息技术 安全技术 抗抵赖 第3部分: 采用非对称技术的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 17964-2021</td> 
   <td class="xl66">信息安全技术 分组密码算法的工作模式</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 25064-2010</td> 
   <td class="xl66">信息安全技术 公钥基础设施 电子签名格式规范</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 25065-2010</td> 
   <td class="xl66">信息安全技术 公钥基础设施 签名生成应用程序的安全要求</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 26855-2011</td> 
   <td class="xl66">信息安全技术 公钥基础设施 证书策略与认证业务声明框架</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 28456-2012</td> 
   <td class="xl66">IPsec协议应用测试规范</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 28457-2012</td> 
   <td class="xl66">SSL协议应用测试规范</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 29241-2012</td> 
   <td class="xl66">信息安全技术 公钥基础设施 PKI互操作性评估准则</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 29243-2012</td> 
   <td class="xl66">信息安全技术 数字证书代理认证路径构造和代理验证规范</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 29767-2013</td> 
   <td class="xl66">信息安全技术 公钥基础设施 桥CA体系证书分级规范</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 30275-2013</td> 
   <td class="xl66">信息安全技术 鉴别与授权 认证中间件框架与接口规范</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 31503-2015</td> 
   <td class="xl66">信息安全技术 电子文档加密与签名消息语法</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 31508-2015</td> 
   <td class="xl66">信息安全技术 公钥基础设施 数字证书策略分类分级规范</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 32213-2015</td> 
   <td class="xl66">信息安全技术 公钥基础设施 远程口令鉴别与密钥建立规范</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 22186-2016</td> 
   <td class="xl66">信息安全技术 具有中央处理器的IC卡芯片安全技术要求</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 15843.1-2017</td> 
   <td class="xl66">信息技术 安全技术 实体鉴别 第1部分：总则</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 15843.2-2017</td> 
   <td class="xl66">信息技术 安全技术 实体鉴别 第2部分：采用对称加密算法的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 15843.3-2023</td> 
   <td class="xl66">信息技术 安全技术 实体鉴别 第3部分: 采用数字签名技术的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 15843.4-2008</td> 
   <td class="xl66">信息技术 安全技术 实体鉴别 第4部分: 采用密码校验函数的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 15843.5-2005</td> 
   <td class="xl66">信息技术 安全技术 实体鉴别 第5部分：使用零知识技术的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 15843.6-2018</td> 
   <td class="xl66">信息技术 安全技术 实体鉴别 第6部分：采用人工数据传递的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 34953.1-2017</td> 
   <td class="xl66">信息技术 安全技术 匿名实体鉴别 第1部分：总则</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 34953.2-2018</td> 
   <td class="xl66">信息技术 安全技术 匿名实体鉴别 第2部分：基于群组公钥签名的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 34953.4-2020</td> 
   <td class="xl66">信息技术 安全技术 匿名实体鉴别 第4部分：基于弱秘密的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 35285-2017</td> 
   <td class="xl66">信息安全技术 公钥基础设施 基于数字证书的可靠电子签名生成及验证技术要求</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 15851.3-2018</td> 
   <td class="xl66">信息技术 安全技术 带消息恢复的数字签名方案 第3部分：基于离散对数的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 36624-2018</td> 
   <td class="xl66">信息技术 安全技术 可鉴别的加密机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 36631-2018</td> 
   <td class="xl66">信息安全技术 时间戳策略和时间戳业务操作规则</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 36644-2018</td> 
   <td class="xl66">信息安全技术 数字签名应用安全证明获取方法</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 15852.1-2020</td> 
   <td class="xl66">信息技术 安全技术 消息鉴别码 第1部分：采用分组密码的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 15852.2-2012</td> 
   <td class="xl66">信息技术 安全技术 消息鉴别码 第2部分：采用专用杂凑函数的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 15852.3-2019</td> 
   <td class="xl66">信息技术 安全技术 消息鉴别码 第3部分：采用泛杂凑函数的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 17901.1-2020</td> 
   <td class="xl66">信息技术 安全技术 密钥管理 第1部分：框架</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 17901.3-2021</td> 
   <td class="xl66">信息技术 安全技术 密钥管理 第3 部分：采用非对称技术的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 25061-2020</td> 
   <td class="xl66">信息安全技术 XML数字签名语法与处理规范</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 38636-2020</td> 
   <td class="xl66">信息安全技术 传输层密码协议（TLCP）</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 38647.1-2020</td> 
   <td class="xl66">信息技术 安全技术 匿名数字签名 第1部分：总则</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 38647.2-2020</td> 
   <td class="xl66">信息技术 安全技术 匿名数字签名 第2部分：采用群组公钥的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 17903.2-2021</td> 
   <td class="xl66">信息技术 安全技术 抗抵赖 第2 部分：采用对称技术的机制</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 17964-2021</td> 
   <td class="xl66">分组密码算法的工作模式</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 30272-2021</td> 
   <td class="xl66">信息安全技术 公钥基础设施 标准符合性测评</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 21053-2023</td> 
   <td class="xl66">信息安全技术 公钥基础设施 PKI系统安全技术要求</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 21054-2023</td> 
   <td class="xl66">信息安全技术 公钥基础设施 PKI系统安全测评方法</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 32922-2023</td> 
   <td class="xl66">信息安全技术 IPSec VPN 安全接入基本要求与实施指南</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 42564-2023</td> 
   <td class="xl66">信息安全技术 边缘计算安全技术要求</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 42570-2023</td> 
   <td class="xl66">信息安全技术 区块链技术安全框架</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 42571-2023</td> 
   <td class="xl66">信息安全技术 区块链信息服务安全规范</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
  <tr > 
   <td class="xl66">GB/T 43207-2023</td> 
   <td class="xl66">信息安全技术 信息系统密码应用设计指南</td> 
   <td class="xl66">　</td> 
   <td class="xl66">　</td> 
  </tr> 
 </tbody>
</table>
</body>


## 免责声明：
本仓库的所有标准和文档均来自密评委和开源项目，旨在为学习和研究提供参考。由于本仓库的内容来源多样，若有涉及侵权或版权问题，请及时联系删除。

## 个人声明：
由于个人的技术水平有限，若仓库中的内容有不准确或不足之处，还请大家提出宝贵意见，感谢大家的支持和理解。

## 侵权声明
本项目包含的所有内容，包括但不限于文档、代码、标准等，均来自网络或开源项目，目的是为学习和研究提供参考。我们尊重所有原作者的版权，若本项目中有任何侵犯版权的内容，敬请及时联系，我们将在确认后第一时间删除相关内容。

请通过以下方式联系我们：
- 邮箱：[yulin.1996@foxmail.com]
我们会尽力确保遵守版权法规，并在必要时进行删除或修改。
感谢您的理解与支持！
