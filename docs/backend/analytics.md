
## Events tracked on Mixpanel


> Name of user  
> Their email address (for marketing emails)  
> Rate of new users added daily, weekly, monthly  
> Number of total users  

```python
mp.people_set(1, {
    "$name": "saurabh Kumar",
    "$email": "saurabh@abc.com",
    "$created": now()
})
```

---

Ref:

- https://mixpanel.com/help/reference/python
- https://docs.google.com/document/d/1fHY6A09Hd-Qg5OFlXbx1k-_nsBRNz3MiSwsP3TMidlA/edit
