# C3D3

No dependencies.

---

C3D3 is a framework that helps to get needed blockchain data from smart-contracts and centralized exchanges. 

It's designed according to a clean architecture. The scalability of the framework is based on it's architecture that provides a simple way to scale up amount of a new adapters and add it to right factories. Each factory is an independent analytical unit and must located at abstract factory. Bridge helps to orchestrate of whole amount of factories and adapters.

# Developer's Preparation

Clone repository:
```
https://github.com/e183b796621afbf902067460/c3d3-framework.git
```

Get into the project folder:
```
cd c3d3-framework/
```

Create `notebooks` folder to store any tests:
```
mkdir notebooks; touch notebook/__init__.py
```

Create virtual environment:
```
python3 -m venv venv
```

And activate it:
```
source venv/bin/activate
```

Install requirements:
```
pip3 install -r requirements.txt
```

# Installation
```
pip install git+https://github.com/e183b796621afbf902067460/c3d3-framework.git#egg=c3d3
```

# Core
This is the layer that holds core-business rules. Also, this layer is the least prone to change. 

Change in any outer layer doesn’t affect this one. Since business rules won’t change often, the change in this layer is very rare. This layer holds entities or core-interfaces. 

An entity can be an object with methods that holds business-logic in it.

# Domain
Rules which are not core-business-rules but essential for this particular framework. 

This layer holds use-cases or wrappers. As the name suggests, it should provide every use-case or particular wrapper of the framework.

# Infrastructure
This is where different modules are coordinated. Also, it holds:
- `Bridges`
- `Abstract Factories`
- `Concrete Factories`
- `Adapters` and `Interfaces`

For some different purposes:
- `Facades`
- `Composites` and `Components`


