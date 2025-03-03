# Will LLMs Scaling Hit the Wall?
## Breaking Barriers with Distributed Resources on Massive Edge Devices

<div align="center">
  <p>
    <a href="#abstract">Abstract</a> |
    <a href="#paper">Paper</a> |
    <a href="https://github.com/tao-shen/Distributed-LLM-Edges">Code</a>
  </p>
</div>

## Authors
- [Tao Shen](https://tao.shen)*
- [Didi Zhu]()*
- [Ziyu Zhao]()*
- [Chao Wu]()
- [Fei Wu]()

Zhejiang University

*Equal contribution

## Abstract

The success of foundation models relies on scaling laws, which show that model performance improves predictably with increased training data and model size. However, this scaling trajectory faces two critical challenges: depletion of high-quality public data and monopolization of computational power required for larger models by tech giants. These bottlenecks severely hinder AI advancement.

In this paper, we advocate leveraging massive distributed edge devices to break through these barriers. We reveal the vast untapped potential of data and computational resources on edge devices, and review recent technical advancements in distributed/federated learning that make this paradigm viable. Our analysis indicates that through edge device collaboration, anyone can participate in training large language models using small edge devices. This shift toward distributed edge training can democratize AI development and foster a more inclusive AI community.

## Key Findings

### Data Resources
- Global data volume is projected to reach 182 ZB by 2025, with IoT devices contributing significantly—increasing from 13.6 ZB in 2019 to 79.4 ZB in 2025
- Smartphone data volume is forecast to grow from 5 EB in 2018 to 8 EB by 2028
- The accumulated smartphone data of the past 5 years (before 2025) is estimated at approximately 33.1 EB

### Computing Power
- The collective computing power of smartphones has grown from 817 EFLOPS in 2020 to 2,758 EFLOPS in 2024
- The cumulative smartphone computing power over the past 5 years totals 9,278 EFLOPS
- Modern flagship devices achieve over 2 TFLOPS per unit, with just 30 current-generation smartphones working in parallel matching the computational capacity of an H100 GPU (59.30 TFLOPS)

## Technical Approaches

1. **Small Language Models at Edges**: Deploy compact language models on resource-constrained devices through model compression, knowledge distillation, and quantization techniques
2. **Collaborative Inference**: Distribute inference across multiple devices to enable running more complex models
3. **Collaborative Training**: Implement model training across distributed devices using federated learning, preserving privacy while leveraging collective computational power

## Societal Impact

- **AI Democratization**: Lower barriers to AI development participation
- **Privacy and Data Ownership**: Protect user data privacy through federated learning
- **Environmental Sustainability**: Utilize idle computing capacity of existing devices, reducing dedicated data center demands

## Citation

```bibtex
@inproceedings{shen2025will,
  title={Will LLMs Scaling Hit the Wall? Breaking Barriers with Distributed Resources on Massive Edge Devices},
  author={Tao Shen and Didi Zhu and Ziyu Zhao and Chao Wu and Fei Wu},
  booktitle={Arxiv},
  year={2025}
}
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.
