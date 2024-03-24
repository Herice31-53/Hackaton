import smartpy as sp


@sp.module
def main():
    class Hackaton(sp.Contract):
        def __init__(self):
            self.data.traceable = True
            self.data.boards = sp.big_map()

        @sp.entrypoint
        def build(self, params):
            sp.cast(params.product, sp.string)
            assert self.data.traceable
            assert not self.data.boards.contains(params.product)
            self.data.boards[params.product] = sp.record(
                deck={
                    'eco': 0,
                    'cost': 0,
                },

            )


        @sp.entrypoint
        def production(self, params):
            sp.cast(params.emission_producer, sp.int)
            sp.cast(params.volume_producer, sp.int)
            sp.cast(params.fixed_costs_producer_per_unit, sp.int)
            sp.cast(params.extra_cost_producer, sp.int)
            assert self.data.traceable
            assert self.data.boards.contains(params.product)
            product_record = self.data.boards[params.product]
            batch_producer = params.volume_producer / 3
            # eco
            product_record.deck['eco'] += params.emission_producer / batch_producer
            # cost
            product_record.deck['cost'] += params.fixed_costs_producer_per_unit + params.extra_cost_producer / params.volume_producer
            #
            self.data.boards[params.product] = product_record
    

        @sp.entrypoint
        def transport(self, params):
            sp.cast(params.emission_transporter, sp.int)
            sp.cast(params.weight_transporter, sp.int)
            sp.cast(params.batch_transporter, sp.int)
            sp.cast(params.distance_transporter, sp.int)
            sp.cast(params.fixed_costs_transporter, sp.int)
            sp.cast(params.cost_per_distance_unit_transporter, sp.int)
            sp.cast(params.time_transporter, sp.int)
            sp.cast(params.cost_per_time_unit_transporter, sp.int)
            assert self.data.traceable
            assert self.data.boards.contains(params.product)
            product_record = self.data.boards[params.product]
            # eco
            product_record.deck['eco'] += params.emission_transporter * params.weight_transporter / (30*params.batch_transporter)
            # cost
            product_record.deck['cost'] += (params.fixed_costs_transporter + params.distance_transporter*params.cost_per_distance_unit_transporter + params.time_transporter*params.cost_per_time_unit_transporter)/ (30*params.batch_transporter)   
            #
            self.data.boards[params.product] = product_record

        @sp.entrypoint
        def transformation(self, params):
            sp.cast(params.emission_transformer, sp.int)
            sp.cast(params.volume_transformer, sp.int)
            sp.cast(params.fixed_costs_transformer_per_unit, sp.int)
            sp.cast(params.extra_cost_transformer, sp.int)
            assert self.data.traceable
            assert self.data.boards.contains(params.product)
            product_record = self.data.boards[params.product]
            # eco
            product_record.deck['eco'] += params.emission_transformer / params.volume_transformer
            # cost
            product_record.deck['cost'] += params.fixed_costs_transformer_per_unit + params.extra_cost_transformer / params.volume_transformer
            #
            self.data.boards[params.product] = product_record

        @sp.entrypoint
        def distribution(self, params):
            sp.cast(params.storage_time_distribution, sp.int)
            sp.cast(params.emission_coefficient_distribution, sp.int)
            sp.cast(params.cost_coefficient_distribution, sp.int)
            assert self.data.traceable
            assert self.data.boards.contains(params.product)
            product_record = self.data.boards[params.product]
            # eco
            product_record.deck['eco'] += params.storage_time_distribution*params.emission_coefficient_distribution
            # cost
            product_record.deck['cost'] += params.storage_time_distribution*params.cost_coefficient_distribution
            #
            self.data.boards[params.product] = product_record

        @sp.entrypoint
        def deleteProduct(self, params):
            del self.data.boards[params.product]

        @sp.entrypoint
        def setPause(self, params):
            self.data.traceable = params


if "main" in __name__:

    @sp.add_test()
    def test():
        # define a contract
        scenario = sp.test_scenario("Hackaton", main)
        c1 = main.Hackaton()

        scenario.h1("Products blockchain")
        # show its representation
        scenario += c1
        scenario.h2("Message execution")
        scenario.h3("Building a contract")

        product1 = "tomatoes"
        
        #producer
        emission_producer = 400000 # grammes of CO2
        volume_producer = 30000
        fixed_costs_producer_per_unit = 1 
        extra_cost_producer = 10000
        
        #transporter
        emission_transporter = 300 #grammes of CO2
        emission_transporter_2 = 150 #grammes of CO2
        weight_transporter = 1200
        batch_transporter=50
        fixed_costs_transporter = 2000
        time_transporter=3
        distance_transporter = 200
        distance_transporter_2 = 100
        cost_per_distance_unit_transporter = 2
        cost_per_time_unit_transporter=2

        #transformer
        emission_transformer = 4800000 # grammes of CO2
        volume_transformer = 100000
        fixed_costs_transformer_per_unit = 1 
        extra_cost_transformer = 100000

        #distribution
        storage_time_distribution = 1 # days
        emission_coefficient_distribution = 1
        cost_coefficient_distribution = 1 
        
        c1.build(product=product1)

        product2 = "apples"
        c1.build(product=product2)
        scenario.h3("deleting a contract")
        c1.deleteProduct(product=product2)

        # producer
        scenario.h3("Production block")
        c1.production(product=product1, emission_producer=emission_producer, volume_producer=volume_producer, fixed_costs_producer_per_unit=fixed_costs_producer_per_unit, extra_cost_producer=extra_cost_producer)
        
        # transporter
        scenario.h3("Transportation block")
        c1.transport(product=product1, emission_transporter=emission_transporter_2, weight_transporter = weight_transporter, batch_transporter=batch_transporter, distance_transporter=distance_transporter, fixed_costs_transporter=fixed_costs_transporter, cost_per_distance_unit_transporter=cost_per_distance_unit_transporter, time_transporter=time_transporter, cost_per_time_unit_transporter=cost_per_time_unit_transporter)

        # transformer
        scenario.h3("Transformation block")
        c1.transformation(product=product1, emission_transformer=emission_transformer, volume_transformer=volume_transformer, fixed_costs_transformer_per_unit=fixed_costs_transformer_per_unit, extra_cost_transformer=extra_cost_transformer)

        # transporter
        scenario.h3("Transportation block")
        c1.transport(product=product1, emission_transporter=emission_transporter, weight_transporter = weight_transporter, batch_transporter=batch_transporter, distance_transporter=distance_transporter_2, fixed_costs_transporter=fixed_costs_transporter, cost_per_distance_unit_transporter=cost_per_distance_unit_transporter, time_transporter=time_transporter, cost_per_time_unit_transporter=cost_per_time_unit_transporter)

        # distributer
        scenario.h3("Distribution block")
        c1.distribution(product=product1, storage_time_distribution=storage_time_distribution, cost_coefficient_distribution=cost_coefficient_distribution, emission_coefficient_distribution=emission_coefficient_distribution)
