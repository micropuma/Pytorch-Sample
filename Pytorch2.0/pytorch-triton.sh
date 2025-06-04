TORCH_LOGS="dynamo,aot,+inductor,bytecode,graph,graph_code,aot_graphs,aot_joint_graph,schedule,fusion,output_code" python pytorch-triton.py \
    2>&1 | tee pytorch-triton.log