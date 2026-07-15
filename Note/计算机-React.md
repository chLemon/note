# React

> [30分钟学会React18核心语法 可能是你学会React最好的机会 前端开发必会框架 无废话精品视频](https://www.bilibili.com/video/BV1pF411m7wV)

## 1. 脚手架建立项目

```shell
# 这个已经废弃了，最新的应该用下面的
npx create-react-app my-app
# 应该用这个了
npx create-next-app my-app
cd my-app
# 启动
npm start
```

项目结构

```text
public      // 静态资源
  ├── favicon.ico
  ├── index.html
  └── manifest.json
src
  ├── App.css
  ├── App.js    // 根组件
  ├── App.test.js
  ├── index.css
  ├── index.js          // 入口文件
  ├── logo.svg
  └── reportWebVitals.js
```

入口文件和根组件是最关键的2个文件，其余的都是可选的，甚至可以删除。

index.js

```javascript
/**
 * 应用入口：挂载 React 根组件到 #root 节点。
 */
import React from "react";          // 关键库1
import ReactDOM from "react-dom/client";    // 关键库2
import App from "./App";    // 根组件，默认是 .js，所以可以不用写后缀
import "./styles/index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(   // 根组件渲染
  <React.StrictMode>    // 严格模式
    <App />
  </React.StrictMode>
);
```

```javascript
// App：应用根组件

function App() {
    // 一个函数
    return (
        <div className="App">
            <h1>Hello React</h1>
        </div>
    );
}

export default App; // 导出函数组件
```

React 有2种组件形式：函数组件、类组件。函数组件是目前主推的，就是上面这种，一个函数，然后导出函数组件。

## 2. JSX 语法

这里直接将 JS 语法和 HTML 语法混合在一起了，这就是 JSX 语法，就是一种模板语法。

```javascript
function App() {
    // 一个函数
    return (
        // 多行时，JSX 语法必须要这个小括号
        <div className="App">
            <h1>Hello React</h1>
        </div>
    );
}
```

JSX 只能返回一个根元素，所以如果想返回多个元素，就需要一个父元素包裹起来。或者用一个空标签

```javascript
function App() {
    return (
        <>
            <h1>Hello React</h1>
            <h2>React is awesome!</h2>
        </>
    );
}
```

注意HTML标签，都需要正确闭合。

## 3. 数据渲染

### 3.1. 插值

用 `{}` 来插入变量。

可以放在标签内容，也可以放在标签属性。

```javascript
function App() {
    // 和组件直接相关的内容，建议直接写在组件里面
    const content = "Hello React！！";
    const id = 1;
    // 这里还可以做一些 js 的逻辑处理
    if (flag) {
        content = <span>Hello React！！！！！</span>;
    } else {
        content = <p>Hello React</p>; // 注意这里，不用写 "" 之类的东西，JSX 不需要做拼接了，直接写 HTML 标签就行了
    }

    return <h1 id={id}>{content}</h1>;
}
```

```javascript
function App() {
    // 数组、列表示例
    const list = [
        { id: 1, name: "React" },
        { id: 2, name: "Vue" },
        { id: 3, name: "Angular" },
    ];
    const listContent = list.map((item) => {
        return <li key={item.id}>{item.name}</li>; // 注意这里，React 要求每个子元素都要有一个唯一的 key 属性，同级唯一即可
    });
    // 这里还可以这么写
    const listContent = list.map(
        (
            item, // 直接写 JSX，注意括号的类型
        ) => <li key={item.id}>{item.name}</li>,
    );

    return <ul>{listContent}</ul>;
}
```

Fragment

如果我们列表要生成多个根标签，那么就要用什么东西包裹一下，如果用之前的空标签，空标签不能设置key，不是一个组件。可以用 Fragment，这个东西就可以当作一个组件来用。

```javascript
function App() {
    const list = [
        { id: 1, name: "React" },
        { id: 2, name: "Vue" },
        { id: 3, name: "Angular" },
    ];
    const listContent = list.map((item) => (
        <Fragment key={item.id}>
            <li>{item.name}</li>
            <li>-----------</li>
        </Fragment>
    ));

    return <ul>{listContent}</ul>;
}
```

### 3.2. 事件操作

JSX 里，属性通常是驼峰

```js
function App() {
    function handleClick(e) {
        // e 可以接受事件信息，可选，比如说鼠标坐标等
        // doing something
    }

    return <button onClick={handleClick}>按钮</button>;
}
```

### 3.3. 状态

函数式组件默认没有状态，需要用 useState

```js
function App() {

    // 不能直接写个变量，然后在事件函数里修改，修改会无效
    // 需要用 useState，里面写默认值，返回值有2个：渲染的内容（读），修改内容的函数（写）
    // 默认值可以是对象，set的时候，会直接赋值。为了方便，js可以写 ...object 来展开对象、数组
    const [content, setContent] = useState('默认值')
    const [data, setData] = useState({
        title: '标题',
        content: '内容演示'
    })

    function handleClick () {
        setContent('新内容')
        setData({
            ...data,
            title: '新的'
        })
    }

    return (
        <div>{content}</div>
        <button onClick={handleClick}>按钮</button>
    )
}
```

## 4. 组件通信

HTML 的标签有一些属性，如 `src`，`img`。这些在 React 里，叫做 Props，有一些和HTML里有一些区别。也可以直接使用JSX的插值来赋值。

例如，`class` 和 js 的关键字重复，改为了 `className`。

width设置时，数字默认单位 px，如果要自己写单位的话，用字符串

### 4.1. 展开

ES6 就直接可以用 `...data` 进行展开，但是必须要放在一个对象字面量里。例如：

```js
console.log({ ...data }); // 是合法的，因为有一个 {}，可以作为对象拷贝
```

```js
return (...data) // JSX 本身作了额外支持，不需要一个 {} 也可以
```

### 4.2. 父组件可以给子组件传值

单向、只读

```js
function Sub (props) {
    return (
        <div>
            <h2>{props.title}</h2>
        </div>
    )
}

function Sub ({title}) { // ES6 提供解构
    return (
        <div>
            <h2>{title}</h2>
        </div>
    )
}

export default function App () {
    return (
        <>
            <Sub title = '标题'/>
        </Sub>
    )
}

```

#### 4.2.1. 插槽

Vue 里有插槽，但是 React 里不需要，直接用 JSX 语法，将 JSX 传递 Props 即可

```js
function List({ children }) {
    // 预定义了一个 children，可以接受 JSX 里，标签内的子元素
    return <ul>{children} // 可以拿到父组件定义的子元素</ul>;
}

export default function App() {
    return (
        <>
            <List>
                {" "}
                // 这里是自定义的一个组件
                <li>列表</li> // 这里是HTML的语法
            </List>
        </>
    );
}
```

### 4.3. 子组件向父组件传值

```js
function Detail({ onActive }) { // 父组件的函数传进来
    const [status, setStatus] = useState(false)
    function handleClick() {
        setStatus(status)
        onActive(status)  // 这里可以调用，把子组件的内容，通过函数传递到父组件
    }
    return (
        // ...
    )
}


export default function App () {
    function handleActive (status) {
        console.log(status)
    }
    return (
        <Detail onActive={handleActive} /> // 这里把 函数传进去
    )
}
```

同级组件，一般也通过父级组件，中转一下。

### 4.4. context hooks

如果传递层级很多，可以通过 Context 来传递。

```js

// 在最顶层定义
const LevelContext = createContext(1) // 要写一个默认值

function Heading() {
    // 在某一个层级里，可以读取使用
    const level = useContext(LevelContext)

    return (
        <Section>
            <LevelContext.Provider value = {level + 1}> // 在 JSX 里这样用，可以设置值
                {children}  // 用 Provider 包裹住所有使用 useContext 的部分
            </LevelContext.Provider>
        </Section>
    )
}
```

## 5. Hooks

之前已经讲了创建状态的 useState 和 传递状态的 useContext

### 5.1. setReducer

我们有可能需要对一个状态，进行多种操作，只用 setState 的话，需要写多个方法：

```js
function App() {
    const [count, setCount] = useState(0)
    const handleIncrement = () => setCount(count + 1)
    const handleDecrement = () => setCount(count - 1)

    return (
        <div>
            <span> {count} </span>
            <button onClick={handleIncrement}>-</button>
            <button onClick={handleDecrement}>+</button>
        </div>
    )
}
```

这样方法就会很多了，对于一个状态的方法，我们可以用 setReducer 统一管理

```js
function countReducer (state, action) {
    switch (action.type) {
        case "increment":
            return state + 1
        case "decrement":
            return state - 1
        default:
            throw new Error()
    }
}

function App() {
    // 一个状态的方法管理在一起。状态当前值，状态修改的触发器
    const [state, dispatch] = useReducer(countReducer, 0)
    const handleIncrement = () => dispatch({type: "increment"})
    const handleDecrement = () => dispatch({type: "decrement"})

    return (
        <div>
            <span> {state} </span>
            <button onClick={handleIncrement}>-</button>
            <button onClick={handleDecrement}>+</button>
        </div>
    )
}
```

### 5.2. setRef

主要2个功能：

1. 记住变更之前的值

```js
const prevCount = useRef()

function handleClick() {
    prevCount.current = count
    // ...
}
```

2. 获取组件，直接操作组件，使用组件方法

```js
const inputRef = useRef(null)

function handleClick() {
    inputRef.current.focus() // inputRef 和 input 标签已经关联在一起了，所以这里可以操作 input 的 DOM 属性
}

return (
    <input type="text" ref={inputRef} /> // 将 input 标签 和 inputRef 通过 ref 关联在一起
)

```

3. 获取子组件。外界直接操作子组件的DOM方法、函数功能

```js
// 这里不能使用下面的写法，必须通过函数表达式的方式定义一个变量，并且要用 forwardRef 方法处理
const Child = forwardRef(function (props, ref) { // 这里接收了父组件传入的 ref
    useImperativeHandle(ref, () => ({ // 上面的ref传进来
        // 暴露给父组件的方法
        myFn: () => {
            console.log('子组件myFn方法')
        }
    }))
    return (
        <div>子组件</div>
    )
})

function App () {
    const childRef = useRef(null)

    function handleClick() {
        childRef.current.myFn()  // 可以通过 childRef 调用子组件的方法
    }

    return (
        <Child ref={childRef} /> // 设置子组件的 ref 属性
    )
}
```

### 5.3. useEffect

设置副作用

```js
// 默认在组件渲染的时候执行
useEffect(() => {
    // ...
}, []) // [] 这里的第二个参数，依赖数组，哪些状态变更函数会执行。现在是空，就是没有，只在渲染时执行。这里传入的状态是 useState 返回的那个
```

### 5.4. useMemo

缓存一些数据，子组件会随着父组件状态变化而变化。父组件重新渲染，子组件默认也会重新渲染。

```js
const result = useMemo(() => {
    // ...
    return result
}, []) // 和 useEffect 类似，依赖数组，传入哪些状态变更时，重新执行里面的内容
```

### 5.5. useCallback

缓存函数。

父组件重新渲染，子组件也会重新渲染。

可以通过

```js
const Buttom = memo(
    function name({onClick}) {
        ...
    }
)
```

来缓存子组件，这样避免子组件的重新渲染。

但是，这里传入了 onClick 函数。父组件重新渲染的时候，会生成新的函数对象，入参不一样了，这里的缓存会失效。所以父组件的函数对象也需要缓存起来。这样子组件的缓存才能有效。

```js
const handleClick = useCallback(
    ...
)
```
