# 爬虫教程 Webscraping Tutorial

## 用 requests BeautifulSoup 爬取豆瓣电影排行

[爬虫入门教程，以豆瓣电影排行为例](https://github.com/hongtaoh/webscraping-tutorial/blob/master/tutorials/douban_movie_250.ipynb)

  - 结果数据：[douban.csv](https://github.com/hongtaoh/webscraping-tutorial/blob/master/data/douban.csv)


## 用 Selenium 爬取 Bilibili 视频信息

[简易 Selenium 教程](https://github.com/hongtaoh/webscraping-tutorial/blob/master/tutorials/selenium-tutorial-bilibili.ipynb)

  - 结果数据：[basketball_videos.csv](https://github.com/hongtaoh/webscraping-tutorial/blob/master/data/basketball_videos.csv)
  


## Selenium 补充信息

### CSS_SELECTOR，多个 attributes

用 `By.CSS_SELECTOR` 时，如果是 `class`, 或者 `id`，很好弄，比如 `div.button`, `div#button`。但如果还有别的各种稀奇古改的 attribute，那么可以这样：`div[class='button'][type='aType']`

### CSS_SELECTOR，A 或者 B

如果你想选多个元素，可以这样：

```
driver.find_elements(By.CSS_SELECTOR, div.class_one, div.class_two)
```

这样，`div.class_one` 或者 `div.class_two` 就会被选中。

参考：https://stackoverflow.com/a/42558060

### 一个元素多个类
如果一个元素的类有两个，比如 `<div class = "a b">`，那么，在定位这个元素时，

  - 如果你用的是 `By.CLASS_NAME`，你需要用 `find_element(By.CLASS_NAME, "a.b")`
  - 如果你用的是 `By.CSS_SELECTOR`，你需要用 `find_element(By.CSS_SELECTOR, "div.a.b")`
  - 如果你用的是 `By.XPATH`，你需要用 `find_element(By.XPATH, '//div[@class="a b"]')`

需要注意的是，用 `CSS_SELECTOR` 时，多个元素你可以只选一个，比如 `find_element(By.CSS_SELECTOR, "div.a")` 但是用 `XPATH` 时，有几个就用几个，也就是说，你只能用 `find_element(By.XPATH, '//div[@class="a b"]')` 而不能用 `find_element(By.XPATH, '//div[@class="a"]')`。

### 多个 child

```html
<div class="initial">
  <div id="first-line">Good 1</div>
  <div id="first-line">Study</div>
    <div class="second-line">Day 1</div>
    <div class="second-line">Day 2</div>
    <div class="second-line">Day 3</div>
    <div class="second-line">Up</div>
      <a href="www.baidu.com">link message here</a>
</div>
```

上面这个结构中，如果我想要的是 "Up"，可以用 `XPATH`:

```
By.XPATH, '//div[@class="initial"]/child::div[2]/child::div[4]'
```

然后 `.get_attribute('innerHTML')`

如果想要的是 link message here:

```
By.XPATH, '//div[@class="initial"]//a'
```

然后 `.get_attribute('innerHTML')` 或者 `.text`。

根据 [Sause Labs 的教程](https://saucelabs.com/resources/articles/selenium-tips-css-selectors)，如果是紧挨着的 child，XPATH 用 `/`，CSS SELECTOR 用 `>`。

不管是不是紧挨着，比如当你想从第一级直接到第三级，比如，从 `div.initial` 直接到 `a`，XPATH 用 `//`，CSS SELECTOR 直接用空格，比如 `div a`

### XPATH 教程

W3Schools 有一个很好的 XPATH 教程：https://www.w3schools.com/xml/xpath_syntax.asp

### Helper function

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException 
```

检查某一个元素是否存在：

```python
def check_exists(ByMethod, value):
    """define the function of checking whether an element exists. 
    Returns true if exists. 
    """

    try:
      wait.until(EC.presence_of_element_located((
        ByMethod, value
      )))
    except (NoSuchElementException, TimeoutException):
      return False
    return True
```

检查多个元素是否存在：

```python
def check_all_exist(ByMethod, value):
    """define the function of checking whether an element exists. 
    Returns true if exists. 
    """
    try:
      wait.until(EC.presence_of_all_elements_located((
        ByMethod, value
      )))
    except (NoSuchElementException, TimeoutException):
      return False
    return True
```

### Time sleep

```python
import random
import time 

# 时间自己定。0.2 表示 0.2 秒
time.sleep(0.2+random.uniform(0, 0.2)) 
```
